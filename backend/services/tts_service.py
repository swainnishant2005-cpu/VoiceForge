from pathlib import Path
from uuid import uuid4
import shutil

from gtts import gTTS
from pydub import AudioSegment


# =========================
# FFMPEG CONFIGURATION
# =========================

FFMPEG_PATH = shutil.which("ffmpeg")
FFPROBE_PATH = shutil.which("ffprobe")

# Make FFmpeg available to pydub
if FFMPEG_PATH:
    AudioSegment.converter = FFMPEG_PATH


# =========================
# AVAILABLE VOICES
# =========================

VOICES = [
    {
        "id": "en",
        "language": "en",
        "name": "English"
    },
    {
        "id": "hi",
        "language": "hi",
        "name": "Hindi"
    },
    {
        "id": "gu",
        "language": "gu",
        "name": "Gujarati"
    },
    {
        "id": "mr",
        "language": "mr",
        "name": "Marathi"
    },
    {
        "id": "es",
        "language": "es",
        "name": "Spanish"
    },
    {
        "id": "fr",
        "language": "fr",
        "name": "French"
    },
    {
        "id": "de",
        "language": "de",
        "name": "German"
    }
]


# =========================
# GET AVAILABLE VOICES
# =========================

def get_available_voices():
    return VOICES


# =========================
# GENERATE SPEECH
# =========================

def generate_speech(
    text: str,
    language: str,
    voice: str,
    speed: float,
    output_directory: Path
):

    # -------------------------
    # Validate voice
    # -------------------------

    selected_voice = next(
        (
            item
            for item in VOICES
            if item["id"] == voice
        ),
        None
    )

    if selected_voice is None:
        raise ValueError(
            "Invalid voice selected."
        )


    # -------------------------
    # Validate language
    # -------------------------

    if selected_voice["language"] != language:
        raise ValueError(
            "Selected voice does not match the selected language."
        )


    # -------------------------
    # Validate speed
    # -------------------------

    if speed < 0.5 or speed > 2.0:
        raise ValueError(
            "Speech speed must be between 0.5x and 2.0x."
        )


    # -------------------------
    # Check FFmpeg
    # -------------------------

    if not FFMPEG_PATH:
        raise RuntimeError(
            "FFmpeg executable was not found."
        )

    if not FFPROBE_PATH:
        raise RuntimeError(
            "FFprobe executable was not found."
        )


    # -------------------------
    # Create output directory
    # -------------------------

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    # -------------------------
    # Create filenames
    # -------------------------

    unique_id = uuid4().hex

    temporary_filename = (
        f"{unique_id}_original.mp3"
    )

    final_filename = (
        f"{unique_id}.mp3"
    )

    temporary_path = (
        output_directory /
        temporary_filename
    )

    final_path = (
        output_directory /
        final_filename
    )


    try:

        # -------------------------
        # Generate speech
        # -------------------------

        speech = gTTS(
            text=text,
            lang=selected_voice["language"],
            slow=False
        )

        speech.save(
            str(temporary_path)
        )


        # -------------------------
        # Load generated MP3
        # -------------------------

        audio = AudioSegment.from_mp3(
            str(temporary_path)
        )


        # -------------------------
        # Apply speed
        # -------------------------

        if speed != 1.0:

            original_frame_rate = audio.frame_rate

            new_frame_rate = int(
                original_frame_rate * speed
            )

            audio = audio._spawn(
                audio.raw_data,
                overrides={
                    "frame_rate": new_frame_rate
                }
            ).set_frame_rate(
                original_frame_rate
            )


        # -------------------------
        # Export final MP3
        # -------------------------

        audio.export(
            str(final_path),
            format="mp3"
        )


        # -------------------------
        # Return filename
        # -------------------------

        return final_filename


    finally:

        # -------------------------
        # Delete temporary file
        # -------------------------

        if temporary_path.exists():
            temporary_path.unlink()