import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_BUCKET = os.getenv(
    "SUPABASE_BUCKET",
    "voiceforge-audio"
)


# =========================
# VALIDATE CONFIGURATION
# =========================

def validate_supabase_config():

    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL is not configured."
        )

    if not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_KEY is not configured."
        )

    if not SUPABASE_BUCKET:
        raise RuntimeError(
            "SUPABASE_BUCKET is not configured."
        )


# =========================
# GET SUPABASE CLIENT
# =========================

def get_supabase_client():
    """
    Kept for compatibility with the existing project.

    The actual audio upload now uses the
    Supabase Storage REST API directly.
    """

    validate_supabase_config()

    from supabase import create_client

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


# =========================
# UPLOAD AUDIO
# =========================

def upload_audio(
    file_path: str,
    filename: str
) -> str:

    validate_supabase_config()

    if not os.path.isfile(file_path):
        raise RuntimeError(
            f"Audio file does not exist: {file_path}"
        )

    # Safely encode the filename for the URL
    encoded_filename = quote(
        filename,
        safe=""
    )

    # Supabase Storage REST upload endpoint
    upload_url = (
        f"{SUPABASE_URL.rstrip('/')}"
        f"/storage/v1/object/"
        f"{SUPABASE_BUCKET}/"
        f"{encoded_filename}"
    )

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "audio/mpeg",
        "cache-control": "3600",
        "x-upsert": "true"
    }

    try:

        # -------------------------
        # Upload MP3
        # -------------------------

        with open(file_path, "rb") as audio_file:

            response = requests.post(
                upload_url,
                headers=headers,
                data=audio_file,
                timeout=60
            )


        # -------------------------
        # Check upload result
        # -------------------------

        if not response.ok:

            print(
                "Supabase upload failed."
            )

            print(
                "Status code:",
                response.status_code
            )

            print(
                "Response:",
                response.text
            )

            raise RuntimeError(
                "Supabase Storage upload failed: "
                f"HTTP {response.status_code} - "
                f"{response.text}"
            )


        print(
            "Supabase upload successful."
        )

        print(
            "Upload response:",
            response.text
        )


        # -------------------------
        # Build public URL
        # -------------------------

        public_url = (
            f"{SUPABASE_URL.rstrip('/')}"
            f"/storage/v1/object/public/"
            f"{SUPABASE_BUCKET}/"
            f"{encoded_filename}"
        )

        print(
            "Supabase public URL:",
            public_url
        )

        return public_url


    except requests.RequestException as error:

        print(
            "Supabase network error:",
            repr(error)
        )

        raise RuntimeError(
            f"Unable to connect to Supabase Storage: {error}"
        ) from error


    except RuntimeError:

        raise


    except Exception as error:

        print(
            "Supabase audio upload error:",
            repr(error)
        )

        raise RuntimeError(
            f"Supabase audio upload failed: {error}"
        ) from error