from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models.user import User

from auth_dependency import get_current_user

from schemas.tts_schema import (
    TTSRequest,
    TTSResponse
)

from services.tts_service import (
    get_available_voices,
    generate_speech
)

from services.storage_service import (
    upload_audio,
    get_supabase_client,
    SUPABASE_BUCKET
)

from routers.usage import (
    check_usage_limit,
    increment_usage
)


router = APIRouter(
    prefix="/api",
    tags=["Text-to-Speech"]
)


# =========================================================
# AUDIO DIRECTORY
# =========================================================

AUDIO_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "generated_audio"
)

AUDIO_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================================================
# GET AVAILABLE VOICES
# =========================================================

@router.get("/voices")
def get_voices():
    return {
        "success": True,
        "voices": get_available_voices()
    }


# =========================================================
# TEXT TO SPEECH
# =========================================================

@router.post(
    "/tts",
    response_model=TTSResponse
)
def text_to_speech(
    request: TTSRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:

        # -------------------------------------------------
        # 1. CHECK DAILY USAGE LIMIT
        # -------------------------------------------------

        check_usage_limit(
            db=db,
            user_id=current_user.id
        )


        # -------------------------------------------------
        # 2. GENERATE SPEECH
        # -------------------------------------------------

        filename = generate_speech(
            text=request.text,
            language=request.language,
            voice=request.voice,
            speed=request.speed,
            output_directory=AUDIO_DIRECTORY
        )


        # -------------------------------------------------
        # 3. GET GENERATED AUDIO FILE
        # -------------------------------------------------

        local_file_path = (
            AUDIO_DIRECTORY / filename
        )


        if not local_file_path.is_file():

            raise RuntimeError(
                "Generated audio file was not found."
            )


        # -------------------------------------------------
        # 4. UPLOAD AUDIO TO SUPABASE
        # -------------------------------------------------

        supabase_url = upload_audio(
            file_path=str(local_file_path),
            filename=filename
        )


        # -------------------------------------------------
        # 5. INCREMENT DAILY USAGE
        # -------------------------------------------------

        increment_usage(
            db=db,
            user_id=current_user.id
        )


        # -------------------------------------------------
        # 6. DELETE LOCAL AUDIO FILE
        # -------------------------------------------------

        if local_file_path.exists():

            local_file_path.unlink()


        # -------------------------------------------------
        # 7. RETURN SUPABASE AUDIO URL
        # -------------------------------------------------

        return {
            "success": True,
            "audio_url": supabase_url
        }


    except HTTPException:

        raise


    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


    except Exception as error:

        print(
            "TTS generation/storage error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate and store speech."
            )
        )


# =========================================================
# AUDIO RETRIEVAL
# =========================================================

@router.get(
    "/audio/{filename}"
)
def get_audio(
    filename: str
):

    # -----------------------------------------------------
    # 1. SECURITY CHECK
    # -----------------------------------------------------

    if (
        Path(filename).name != filename
        or not filename.endswith(".mp3")
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid audio filename."
        )


    # -----------------------------------------------------
    # 2. CHECK LOCAL FILE
    # -----------------------------------------------------

    file_path = (
        AUDIO_DIRECTORY / filename
    )


    if file_path.is_file():

        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )


    # -----------------------------------------------------
    # 3. GET AUDIO FROM SUPABASE
    # -----------------------------------------------------

    try:

        client = get_supabase_client()

        public_url = (
            client
            .storage
            .from_(SUPABASE_BUCKET)
            .get_public_url(filename)
        )


        if not public_url:

            raise HTTPException(
                status_code=404,
                detail="Audio file not found."
            )


        return RedirectResponse(
            url=public_url
        )


    except HTTPException:

        raise


    except Exception as error:

        print(
            "Supabase audio retrieval error:",
            error
        )

        raise HTTPException(
            status_code=404,
            detail="Audio file not found."
        )