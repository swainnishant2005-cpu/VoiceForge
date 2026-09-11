from pathlib import Path
from uuid import uuid4
import os

from gtts import gTTS
from pydub import AudioSegment


# =========================
# FFMPEG CONFIGURATION
# =========================

FFMPEG_BIN = (
    r"C:\Users\Nishant Swain\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.1-full_build-shared\bin"
)

FFMPEG_PATH = os.path.join(
    FFMPEG_BIN,
    "ffmpeg.exe"
)

FFPROBE_PATH = os.path.join(
    FFMPEG_BIN,
    "ffprobe.exe"
)


# Make FFmpeg tools available to pydub
os.environ["PATH"] = (
    FFMPEG_BIN
    + os.pathsep
    + os.environ.get("PATH", "")
)


# Tell pydub exactly where FFmpeg is
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

    if not os.path.isfile(FFMPEG_PATH):
        raise RuntimeError(
            "FFmpeg executable was not found."
        )

    if not os.path.isfile(FFPROBE_PATH):
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

            new_frame_rate = int(
                audio.frame_rate * speed
            )

            audio = audio._spawn(
                audio.raw_data,
                overrides={
                    "frame_rate":
                    new_frame_rate
                }
            ).set_frame_rate(
                audio.frame_rate
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