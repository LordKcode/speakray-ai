from fastapi import FastAPI
from pydantic import BaseModel
from app.backend.conversation import add_message, get_conversation

app = FastAPI(title="SpeakRay AI")


class ConversationRequest(BaseModel):
    message: str
    session_id: str


@app.get("/")
def home():
    return {
        "message": "Welcome to SpeakRay AI!",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SpeakRay AI"
    }


@app.post("/conversation")
def conversation(request: ConversationRequest):
    reply = "I received your message. SpeakRay AI is listening!"

    add_message(
        request.session_id,
        request.message,
        reply
    )

    return {
        "session_id": request.session_id,
        "user_message": request.message,
        "reply": reply
    }

@app.get("/conversation/{session_id}")
def get_conversation_history(session_id: str):
    return {
        "session_id": session_id,
        "messages": get_conversation(session_id)
    }