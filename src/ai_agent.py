from typing import TypedDict, Optional, List, Dict, Any
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from src.prompts import SYSTEM_PROMPT
from src.storage_helper import R2Storage

load_dotenv()

class AI_Agent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm = init_chat_model(os.getenv("LLM_MODEL", "google-genai"), temperature=0.1)
        self.system_prompt = SYSTEM_PROMPT
        self.storage = R2Storage("solutions-architect")

    def get_response(self, user_message: str, user_id: Optional[str] = None) -> str:
        try:
            context = ""
            if user_id:
                context = self.get_chat_context(user_id)
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {user_message}" if context else user_message)
            ]
            response = self.llm(messages)
            
            if user_id:
                self.save_chat_history(user_id, user_message, response.content)
            
            return response.content
        except Exception as e:
            print(f"Error: {e}")
            return "Error processing request."

    def get_chat_context(self, user_id: str) -> str:
        history = self.storage.get_history(user_id)
        return "\n".join([f"U: {c['user_message']}\nA: {c['bot_response'][:100]}" for c in history[-5:]])

    def save_chat_history(self, user_id: str, user_message: str, bot_response: str):
        history = self.storage.get_history(user_id)
        history.append({'user_message': user_message, 'bot_response': bot_response, 'timestamp': datetime.now(timezone.utc).isoformat()})
        self.storage.save_history(user_id, history)

    def get_user_chat_history(self, user_id: str, limit: int = 10):
        history = self.storage.get_history(user_id)
        return history[-limit:]

    def delete_user_chat_history(self, user_id: str):
        self.storage.delete_history(user_id)
        return True

def main():
    agent = AI_Agent(os.getenv("GOOGLE_API_KEY"))
    print(agent.get_response(input("Ask Architect: ")))

if __name__ == "__main__":
    main()
