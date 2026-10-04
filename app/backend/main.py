from fastapi import FastAPI

app = FastAPI(title="SpeakRay AI")


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