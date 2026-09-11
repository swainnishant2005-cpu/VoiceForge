from pydantic import BaseModel, Field


class TTSRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to convert into speech"
    )

    language: str = Field(
        ...,
        description="Language code, for example en or hi"
    )

    voice: str = Field(
        ...,
        description="Voice identifier"
    )

    speed: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Speech speed from 0.5x to 2.0x"
    )


class TTSResponse(BaseModel):

    success: bool

    audio_url: str