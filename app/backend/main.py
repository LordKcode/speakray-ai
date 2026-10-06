from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="SpeakRay AI")


class ConversationRequest(BaseModel):
    message: str


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
    return {
        "user_message": request.message,
        "reply": "I received your message. SpeakRay AI is listening!"
    }