from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.favorite import Favorite
from models.speech_history import SpeechHistory

from auth_dependency import get_current_user


router = APIRouter(
    prefix="/api/favorites",
    tags=["Favorites"]
)


# =========================
# ADD / REMOVE FAVORITE
# =========================

@router.post("/{history_id}")
def add_favorite(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check whether speech history exists
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

    # Check whether already favorited
    existing_favorite = (
        db.query(Favorite)
        .filter(
            Favorite.history_id == history_id,
            Favorite.user_id == current_user.id
        )
        .first()
    )

    if existing_favorite:
        return {
            "success": True,
            "message": "Speech is already in favorites.",
            "favorite": True
        }

    favorite = Favorite(
        user_id=current_user.id,
        history_id=history_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {
        "success": True,
        "message": "Speech added to favorites.",
        "favorite": True,
        "favorite_id": favorite.id
    }


# =========================
# GET FAVORITES
# =========================

@router.get("")
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    favorites = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id
        )
        .order_by(
            Favorite.created_at.desc()
        )
        .all()
    )

    result = []

    for favorite in favorites:

        history_item = (
            db.query(SpeechHistory)
            .filter(
                SpeechHistory.id == favorite.history_id
            )
            .first()
        )

        if history_item is None:
            continue

        result.append({
            "favorite_id": favorite.id,
            "history_id": history_item.id,
            "text": history_item.text,
            "language": history_item.language,
            "voice": history_item.voice,
            "speed": history_item.speed,
            "audio_filename": history_item.audio_filename,
            "created_at": favorite.created_at.isoformat()
        })

    return {
        "success": True,
        "favorites": result
    }


# =========================
# REMOVE FAVORITE
# =========================

@router.delete("/{history_id}")
def remove_favorite(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    favorite = (
        db.query(Favorite)
        .filter(
            Favorite.history_id == history_id,
            Favorite.user_id == current_user.id
        )
        .first()
    )

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found."
        )

    db.delete(favorite)
    db.commit()

    return {
        "success": True,
        "message": "Speech removed from favorites.",
        "favorite": False
    }