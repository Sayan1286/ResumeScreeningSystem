import re
from pathlib import Path

import fitz
from docx import Document


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


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


def extract_candidate_email(text: str) -> str | None:
    match = EMAIL_PATTERN.search(text)

    if match is None:
        return None

    return match.group(0)


def extract_candidate_name(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    email = extract_candidate_email(text)

    for line in lines[:10]:
        if email and email.lower() in line.lower():
            continue

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line,
        ).strip()

        words = cleaned.split()

        if 2 <= len(words) <= 5:
            if all(
                word.replace("-", "").replace("'", "").isalpha()
                for word in words
            ):
                return cleaned

    return None


def extract_candidate_details(
    text: str,
) -> tuple[str | None, str | None]:
    candidate_name = extract_candidate_name(text)
    candidate_email = extract_candidate_email(text)

    return candidate_name, candidate_email


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