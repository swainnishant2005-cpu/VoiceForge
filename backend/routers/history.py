from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.speech_history import SpeechHistory
from auth_dependency import get_current_user

from schemas.history_schema import (
    SpeechHistoryCreate,
    SpeechHistoryResponse
)


router = APIRouter(
    prefix="/api/history",
    tags=["Speech History"]
)


# =========================================================
# GET USER SPEECH HISTORY
# =========================================================

@router.get(
    "",
    response_model=list[SpeechHistoryResponse]
)
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = (
        db.query(SpeechHistory)
        .filter(
            SpeechHistory.user_id == current_user.id
        )
        .order_by(
            SpeechHistory.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": item.id,
            "text": item.text,
            "language": item.language,
            "voice": item.voice,
            "speed": item.speed,
            "audio_filename": item.audio_filename,
            "created_at": item.created_at.isoformat()
        }
        for item in history
    ]


# =========================================================
# CREATE SPEECH HISTORY
# =========================================================

@router.post(
    "",
    response_model=SpeechHistoryResponse,
    status_code=201
)
def create_history(
    request: SpeechHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history_item = SpeechHistory(
        user_id=current_user.id,
        text=request.text,
        language=request.language,
        voice=request.voice,
        speed=request.speed,
        audio_filename=request.audio_filename
    )

    db.add(history_item)
    db.commit()
    db.refresh(history_item)

    return {
        "id": history_item.id,
        "text": history_item.text,
        "language": history_item.language,
        "voice": history_item.voice,
        "speed": history_item.speed,
        "audio_filename": history_item.audio_filename,
        "created_at": history_item.created_at.isoformat()
    }


# =========================================================
# DELETE SPEECH HISTORY
# =========================================================

@router.delete("/{history_id}")
def delete_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history_item = (
        db.query(SpeechHistory)
        .filter(
            SpeechHistory.id == history_id,
            SpeechHistory.user_id == current_user.id
        )
        .first()
    )

    if history_item is None:
        raise HTTPException(
            status_code=404,
            detail="Speech history item not found."
        )

    db.delete(history_item)
    db.commit()

    return {
        "success": True,
        "message": "Speech history deleted successfully."
    }
# CLEAR ALL USER SPEECH HISTORY
@router.delete("")
def clear_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_count = (
        db.query(SpeechHistory)
        .filter(
            SpeechHistory.user_id == current_user.id
        )
        .delete(
            synchronize_session=False
        )
    )

    db.commit()

    return {
        "success": True,
        "message": "All speech history cleared successfully.",
        "deleted_count": deleted_count
    }