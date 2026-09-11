import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv(
    "SUPABASE_BUCKET",
    "voiceforge-audio"
)


def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Supabase environment variables are not configured."
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


def upload_audio(
    file_path: str,
    filename: str
) -> str:

    client = get_supabase_client()

    with open(file_path, "rb") as file:
        client.storage.from_(
            SUPABASE_BUCKET
        ).upload(
            path=filename,
            file=file,
            file_options={
                "content-type": "audio/mpeg",
                "cache-control": "3600",
                "upsert": "false"
            }
        )

    public_url = client.storage.from_(
        SUPABASE_BUCKET
    ).get_public_url(filename)

    return public_url