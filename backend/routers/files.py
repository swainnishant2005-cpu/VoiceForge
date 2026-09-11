from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from models.user import User
from auth_dependency import get_current_user
from services.file_service import extract_text_from_file


router = APIRouter(
    prefix="/api/files",
    tags=["File Upload"]
)


UPLOAD_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "uploaded_files"
)

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/extract")
async def extract_file_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    # =========================================================
    # CHECK FILE NAME
    # =========================================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a file."
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only TXT, PDF, and DOCX files are allowed."
            )
        )

    # =========================================================
    # SAVE FILE
    # =========================================================

    safe_filename = Path(
        file.filename
    ).name

    file_path = (
        UPLOAD_DIRECTORY
        / safe_filename
    )

    try:

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size cannot exceed 10 MB."
            )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(contents)

        # =====================================================
        # EXTRACT TEXT
        # =====================================================

        extracted_text = extract_text_from_file(
            file_path=str(file_path),
            filename=safe_filename
        )

        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the file."
            )

        # =====================================================
        # LIMIT TEXT
        # =====================================================

        if len(extracted_text) > 5000:

            extracted_text = extracted_text[:5000]

        return {
            "success": True,
            "filename": safe_filename,
            "text": extracted_text,
            "characters": len(extracted_text)
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
            "File extraction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to extract text from the file."
        )

    finally:

        # =====================================================
        # DELETE TEMPORARY FILE
        # =====================================================

        if file_path.exists():

            try:
                file_path.unlink()

            except Exception:
                pass