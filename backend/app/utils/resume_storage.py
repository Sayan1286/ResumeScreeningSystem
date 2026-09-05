from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = settings.max_resume_size_mb * 1024 * 1024


def validate_resume_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed",
        )

    return extension


def generate_stored_filename(extension: str) -> str:
    return f"{uuid4().hex}{extension}"


def get_upload_directory() -> Path:
    directory = Path(settings.upload_directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


async def save_resume_file(
    file: UploadFile,
    stored_filename: str,
) -> tuple[str, int]:
    directory = get_upload_directory()
    file_path = directory / stored_filename

    total_size = 0

    try:
        with file_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    file_path.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=(
                            f"Resume file size cannot exceed "
                            f"{settings.max_resume_size_mb} MB"
                        ),
                    )

                output.write(chunk)
    finally:
        await file.close()

    return str(file_path), total_size