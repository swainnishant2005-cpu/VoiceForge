from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.tts import router as tts_router
from database import Base, engine
from models.user import User
from routers.auth import router as auth_router
from models.speech_history import SpeechHistory
from routers.history import router as history_router
from routers.ai import router as ai_router
from routers.files import router as files_router
from models.favorite import Favorite
from routers.favorites import router as favorites_router
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="VoiceForge Text-to-Speech API",
    description="A full-stack Text-to-Speech application using React and FastAPI.",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://voice-forge-frontend.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================

app.include_router(tts_router)
app.include_router(auth_router)
app.include_router(history_router)
app.include_router(ai_router)
app.include_router(files_router)
app.include_router(favorites_router)

# =========================
# ROOT
# =========================

@app.get("/")
def home():
    return {
        "message": "VoiceForge Text-to-Speech API is running"
    }