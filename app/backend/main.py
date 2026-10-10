import os

from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the environment.")

client = genai.Client(api_key=api_key)
from app.backend.conversation import add_message, get_conversation
from database.db import (
    initialize_database,
    get_all_sessions,
    delete_conversation
)

app = FastAPI(title="SpeakRay AI")
initialize_database()


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
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=request.message
        )

        reply = response.text

        if not reply:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response."
            )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="SpeakRay could not get an AI response. Please try again."
        )

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

@app.get("/conversations")
def list_conversations():
    return {
        "conversations": get_all_sessions()
    }

@app.delete("/conversation/{session_id}")
def delete_conversation_history(session_id: str):
    deleted_count = delete_conversation(session_id)

    return {
        "session_id": session_id,
        "deleted_messages": deleted_count,
        "message": "Conversation deleted successfully"
        if deleted_count > 0
        else "No conversation found for this session"
    }