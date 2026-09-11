from fastapi import APIRouter, Depends, HTTPException

from models.user import User
from auth_dependency import get_current_user

from schemas.ai_schema import (
    AIEnhanceRequest,
    AIEnhanceResponse
)

from services.ai_service import enhance_text


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Enhancement"]
)


@router.post(
    "/enhance",
    response_model=AIEnhanceResponse
)
def enhance_text_endpoint(
    request: AIEnhanceRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        enhanced_text = enhance_text(
            text=request.text,
            action=request.action
        )

        return {
            "success": True,
            "original_text": request.text,
            "enhanced_text": enhanced_text,
            "action": request.action
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        print("AI enhancement error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to enhance text."
        )