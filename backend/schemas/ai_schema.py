from pydantic import BaseModel, Field


class AIEnhanceRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to enhance"
    )

    action: str = Field(
        ...,
        description="Enhancement action"
    )


class AIEnhanceResponse(BaseModel):
    success: bool
    original_text: str
    enhanced_text: str
    action: str