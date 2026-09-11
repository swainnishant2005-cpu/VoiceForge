from pydantic import BaseModel


class SpeechHistoryCreate(BaseModel):
    text: str
    language: str
    voice: str
    speed: float
    audio_filename: str


class SpeechHistoryResponse(BaseModel):
    id: int
    text: str
    language: str
    voice: str
    speed: float
    audio_filename: str
    created_at: str