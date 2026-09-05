from pathlib import Path

import fitz
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    pdf_bytes = Path(file_path).read_bytes()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    try:
        pages_text = [
            page.get_text()
            for page in document
        ]

        return "\n".join(pages_text).strip()
    finally:
        document.close()


def extract_docx_text(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_resume_text(
    file_path: str,
    file_type: str,
) -> str:
    extension = Path(file_path).suffix.lower()

    if file_type.lower() == "pdf" or extension == ".pdf":
        return extract_pdf_text(file_path)

    if file_type.lower() == "docx" or extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(
        f"Unsupported resume file type: {file_type}"
    )