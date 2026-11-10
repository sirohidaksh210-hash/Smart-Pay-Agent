"""
FastAPI backend for SmartPay Agent.
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from agent import chat_with_agent

app = FastAPI(
    title="SmartPay Agent API",
    description="AI-powered PayPal business assistant backend",
    version="1.0.0",
)

# Allow requests from the React frontend (localhost:3000 or 5173 for Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str
    success: bool = True


@app.get("/")
async def root():
    return {
        "app": "SmartPay Agent",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok", "message": "SmartPay Agent is live 🚀"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts a user message + conversation history,
    runs it through the Gemini agent, returns the AI response.
    """
    try:
        history = [{"role": m.role, "content": m.content} for m in request.history]
        response = await chat_with_agent(request.message, history)
        return ChatResponse(response=response, success=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
