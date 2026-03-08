from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time
from collections import defaultdict
import os
import traceback
from dotenv import load_dotenv

# Load environment variables from the root or from src/
load_dotenv() # checks root
load_dotenv(os.path.join(os.path.dirname(__file__), "src", ".env")) # checks src/

from src.ai_agent import AI_Agent

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Allow CORS for local and deployment origins
allowed_origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "https://solutions-architect-agent-752583171069.asia-southeast1.run.app",
    "https://solutions-architect-agent-948325778469.northamerica-northeast2.run.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Jinja2 templates and static files
templates = Jinja2Templates(directory="templates")

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple in-memory rate limiter: {ip: [timestamps]}
rate_limit_window = 60  # seconds
rate_limit_count = 10
rate_limit_data = defaultdict(list)

# Define the request model for chat messages
class ChatRequest(BaseModel):
    message: str
    user_id: str = None

# Define the request model for chat history
class ChatHistoryRequest(BaseModel):
    user_id: str
    limit: int = 10

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to log tracebacks"""
    print(f"ERROR: Unhandled exception in {request.method} {request.url}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc() if os.getenv("DEBUG") else None}
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: Request, chat: ChatRequest):
    client_ip = request.client.host
    now = time.time()
    timestamps = rate_limit_data[client_ip]
    # Remove timestamps outside the window
    rate_limit_data[client_ip] = [t for t in timestamps if now - t < rate_limit_window]
    if len(rate_limit_data[client_ip]) >= rate_limit_count:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait.")
    rate_limit_data[client_ip].append(now)

    # Use AI agent to generate response
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in environment variables.")
    
    agent = AI_Agent(api_key)
    response = agent.get_response(chat.message, chat.user_id)
    return JSONResponse({
        "response": response
    })

@app.post("/chat-history")
async def get_chat_history(request: Request, history_request: ChatHistoryRequest):
    """Get user's chat history"""
    print(f"Received chat history request: {history_request}")
    client_ip = request.client.host
    now = time.time()
    timestamps = rate_limit_data[client_ip]
    # Remove timestamps outside the window
    rate_limit_data[client_ip] = [t for t in timestamps if now - t < rate_limit_window]
    if len(rate_limit_data[client_ip]) >= rate_limit_count:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait.")
    rate_limit_data[client_ip].append(now)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in environment variables.")
    
    agent = AI_Agent(api_key)
    history = agent.get_user_chat_history(history_request.user_id, history_request.limit)
    print(f"Returning {len(history)} chat history entries")
    return JSONResponse({
        "history": history
    })

@app.delete("/chat-history")
async def delete_chat_history(request: Request, history_request: ChatHistoryRequest):
    """Delete user's chat history"""
    client_ip = request.client.host
    now = time.time()
    timestamps = rate_limit_data[client_ip]
    # Remove timestamps outside the window
    rate_limit_data[client_ip] = [t for t in timestamps if now - t < rate_limit_window]
    if len(rate_limit_data[client_ip]) >= rate_limit_count:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait.")
    rate_limit_data[client_ip].append(now)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in environment variables.")
    
    agent = AI_Agent(api_key)
    success = agent.delete_user_chat_history(history_request.user_id)
    return JSONResponse({
        "success": success,
        "message": "Chat history deleted successfully" if success else "Failed to delete chat history"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
