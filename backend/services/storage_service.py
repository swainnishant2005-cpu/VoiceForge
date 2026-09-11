import os

from dotenv import load_dotenv
from supabase import create_client


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
# GET SUPABASE CLIENT
# =========================

def get_supabase_client():

    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL is not configured."
        )

    if not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_KEY is not configured."
        )

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

    client = get_supabase_client()

    try:

        # -------------------------
        # Upload file
        # -------------------------

        with open(file_path, "rb") as file:

            response = (
                client
                .storage
                .from_(SUPABASE_BUCKET)
                .upload(
                    path=filename,
                    file=file,
                    file_options={
                        "content-type": "audio/mpeg",
                        "cache-control": "3600",
                        "upsert": "true"
                    }
                )
            )

        print(
            "Supabase upload response:",
            response
        )


        # -------------------------
        # Generate public URL
        # -------------------------

        public_url = (
            client
            .storage
            .from_(SUPABASE_BUCKET)
            .get_public_url(filename)
        )

        print(
            "Supabase public URL:",
            public_url
        )


        if not public_url:
            raise RuntimeError(
                "Supabase did not return a public URL."
            )


        return str(public_url)


    except Exception as error:

        print(
            "Supabase upload error:",
            repr(error)
        )

        # Print the underlying exception if
        # Supabase has wrapped another error.
        if error.__context__:
            print(
                "Underlying Supabase error:",
                repr(error.__context__)
            )

        raise RuntimeError(
            f"Supabase audio upload failed: {error}"
        ) from error