from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.usage import Usage
from auth_dependency import get_current_user


router = APIRouter(
    prefix="/api",
    tags=["Usage"]
)


# =========================================================
# DAILY USAGE LIMIT
# =========================================================

DAILY_USAGE_LIMIT = 10


# =========================================================
# GET CURRENT DAILY USAGE
# =========================================================

@router.get("/usage")
def get_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    usage = (
        db.query(Usage)
        .filter(
            Usage.user_id == current_user.id,
            Usage.usage_date == today
        )
        .first()
    )

    if usage is None:
        used = 0
    else:
        used = usage.speech_count

    remaining = max(
        DAILY_USAGE_LIMIT - used,
        0
    )

    return {
        "used": used,
        "limit": DAILY_USAGE_LIMIT,
        "remaining": remaining
    }


# =========================================================
# CHECK DAILY USAGE LIMIT
# =========================================================

def check_usage_limit(
    db: Session,
    user_id: int
):
    today = date.today()

    usage = (
        db.query(Usage)
        .filter(
            Usage.user_id == user_id,
            Usage.usage_date == today
        )
        .first()
    )

    if usage is not None:

        if usage.speech_count >= DAILY_USAGE_LIMIT:

            raise HTTPException(
                status_code=429,
                detail=(
                    "Daily speech generation limit "
                    "reached. Please try again tomorrow."
                )
            )


# =========================================================
# INCREMENT DAILY USAGE
# =========================================================

def increment_usage(
    db: Session,
    user_id: int
):
    today = date.today()

    usage = (
        db.query(Usage)
        .filter(
            Usage.user_id == user_id,
            Usage.usage_date == today
        )
        .first()
    )

    if usage is None:

        usage = Usage(
            user_id=user_id,
            usage_date=today,
            speech_count=1
        )

        db.add(usage)

    else:

        usage.speech_count += 1

    db.commit()