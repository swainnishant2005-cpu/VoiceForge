from pathlib import Path

from pypdf import PdfReader
from docx import Document


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


def extract_text_from_file(
    file_path: str,
    filename: str
) -> str:

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Only TXT, PDF, and DOCX files are allowed."
        )

    # =========================================================
    # TXT FILE
    # =========================================================

    if extension == ".txt":

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        except UnicodeDecodeError:

            with open(
                file_path,
                "r",
                encoding="latin-1"
            ) as file:

                text = file.read()

        return text.strip()

    # =========================================================
    # PDF FILE
    # =========================================================

    if extension == ".pdf":

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                pages.append(page_text)

        return "\n\n".join(pages).strip()

    # =========================================================
    # DOCX FILE
    # =========================================================

    if extension == ".docx":

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                paragraphs.append(
                    paragraph.text.strip()
                )

        return "\n\n".join(paragraphs).strip()

    return ""