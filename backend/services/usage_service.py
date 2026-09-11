from datetime import date

from sqlalchemy.orm import Session

from models.usage import Usage


DAILY_LIMIT = 10


def get_today_usage(
    db: Session,
    user_id: int
) -> Usage:

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
            speech_count=0
        )

        db.add(usage)
        db.commit()
        db.refresh(usage)

    return usage


def check_usage_limit(
    db: Session,
    user_id: int
) -> Usage:

    usage = get_today_usage(
        db=db,
        user_id=user_id
    )

    if usage.speech_count >= DAILY_LIMIT:
        raise ValueError(
            f"Daily speech generation limit of "
            f"{DAILY_LIMIT} has been reached."
        )

    return usage


def increment_usage(
    db: Session,
    user_id: int
) -> Usage:

    usage = get_today_usage(
        db=db,
        user_id=user_id
    )

    usage.speech_count += 1

    db.commit()
    db.refresh(usage)

    return usage