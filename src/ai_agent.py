from datetime import datetime, timezone
from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import os
from dotenv import load_dotenv

# Import the system prompt from prompts module
from src.prompts import SYSTEM_PROMPT

# Initialize LangSmith tracing if configured
from src.langsmith_debug import LANGSMITH_API_KEY,LANGSMITH_ENDPOINT,LANGSMITH_PROJECT,LANGSMITH_TRACING

# Load environment variables from .env file
load_dotenv()

# setting up Firestore for caching
from firebase_admin import firestore, initialize_app
initialize_app()
db = firestore.client()

import hashlib

class AgentState(TypedDict):
    messages: list

class AI_Agent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm = init_chat_model(os.getenv("LLM_MODEL"), temperature=0.1)
        self.system_prompt = SYSTEM_PROMPT

    def get_user_id(self, user_fingerprint: str) -> str:
        """Generate a consistent user ID from browser fingerprint"""
        return hashlib.sha256(user_fingerprint.encode()).hexdigest()[:16]

    def get_chat_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve recent chat history for context"""
        try:
            print(f"Getting chat history for user_id: {user_id}")
            
            # Get chat history from last 7 days
            from datetime import timedelta
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)
            
            chats = db.collection("sa-chat-history").where("user_id", "==", user_id).where("timestamp", ">=", cutoff_date).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            history = []
            for chat in chats:
                data = chat.to_dict()
                timestamp = data.get("timestamp")
                # Convert Firestore timestamp to ISO format for JavaScript
                if timestamp:
                    timestamp_iso = timestamp.isoformat() if hasattr(timestamp, 'isoformat') else str(timestamp)
                else:
                    timestamp_iso = datetime.now(timezone.utc).isoformat()
                    
                history.append({
                    "user_message": data.get("user_message"),
                    "ai_response": data.get("ai_response"),
                    "timestamp": timestamp_iso
                })
            
            print(f"Found {len(history)} chat history entries")
            return list(reversed(history))  # Return in chronological order
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            import traceback
            traceback.print_exc()
            return []

    def store_chat_history(self, user_id: str, user_message: str, ai_response: str):
        """Store chat interaction for future context"""
        try:
            print(f"Storing chat history for user_id: {user_id}")
            
            result = db.collection("sa-chat-history").add({
                "user_id": user_id,
                "user_message": user_message,
                "ai_response": ai_response,
                "timestamp": datetime.now(timezone.utc)
            })
            print(f"Chat history stored successfully with ID: {result[1].id}")
        except Exception as e:
            print(f"Error storing chat history: {e}")
            import traceback
            traceback.print_exc()

    def get_response(self, user_message: str, user_id: str = None) -> str:
        # Use a hash of the user message as the cache key
        cache_key = f"ai_response:{hashlib.sha256(user_message.encode()).hexdigest()}"
        
        # Check cache only if Firebase is initialized
        cached_response = None
        if db is not None:
            try:
                cached = db.collection("cache").document(cache_key).get()
                if cached.exists:
                    data = cached.to_dict()
                    expires = data.get("expires")
                    if expires and expires > datetime.now(timezone.utc):
                        cached_response = data.get("response")
                        print("Using cached response")
                    else:
                        # Optionally delete expired cache
                        db.collection("cache").document(cache_key).delete()
            except Exception as e:
                print(f"Error checking cache: {e}")
        
        # If we have a cached response, use it
        if cached_response:
            # Store cached response in user's chat history
            if user_id:
                self.store_chat_history(user_id, user_message, cached_response)
            return cached_response
        
        # Generate new response if not cached
        # Get chat history for context if user ID is provided
        messages = [SystemMessage(content=self.system_prompt)]
        
        if user_id:
            chat_history = self.get_chat_history(user_id, limit=5)  # Last 5 conversations
            if chat_history:
                # Add context from previous conversations
                context_message = "Previous conversation context:\n"
                for chat in chat_history:
                    context_message += f"User: {chat['user_message']}\nAssistant: {chat['ai_response'][:200]}...\n\n"
                
                messages.append(HumanMessage(content=f"[CONTEXT] {context_message}"))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        response = self.llm(messages)
        
        # Store the response in Firestore cache with 1-month expiration
        if db is not None:
            try:
                from datetime import timedelta
                db.collection("cache").document(cache_key).set({
                    "response": response.content,
                    "expires": datetime.now(timezone.utc) + timedelta(days=30)  # Extended to 1 month
                })
            except Exception as e:
                print(f"Error storing cache: {e}")
        
        # Store chat history for future context
        if user_id:
            self.store_chat_history(user_id, user_message, response.content)
        
        return response.content

    def get_user_chat_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's chat history for display purposes"""
        return self.get_chat_history(user_id, limit)

    def delete_user_chat_history(self, user_id: str) -> bool:
        """Delete all chat history for a user"""
        try:
            if db is None:
                print("Firebase not initialized, cannot delete chat history")
                return False
                
            print(f"Deleting chat history for user_id: {user_id}")
            
            # Get all chat history documents for this user
            chats = db.collection("sa-chat-history").where("user_id", "==", user_id).stream()
            
            # Delete all documents
            for chat in chats:
                db.collection("sa-chat-history").document(chat.id).delete()
            
            return True
        except Exception as e:
            print(f"Error deleting chat history: {e}")
            return False

def main():

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment variables.")
        return
    

    agent = AI_Agent(api_key)
    user_input = input("Ask your cloud architecture question: ")
    print(agent.get_response(user_input))

if __name__ == "__main__":
    main()