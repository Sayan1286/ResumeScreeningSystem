from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_parser import (
    extract_candidate_details,
    extract_resume_text,
)
from app.utils.resume_storage import (
    generate_stored_filename,
    save_resume_file,
    validate_resume_file,
)


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    job_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.recruiter_id == current_user.id,
        )
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    extension = validate_resume_file(file)
    stored_filename = generate_stored_filename(extension)

    file_path, file_size = await save_resume_file(
        file,
        stored_filename,
    )

    try:
        extracted_text = extract_resume_text(
            file_path,
            extension.lstrip("."),
        )
    except Exception:
        Path(file_path).unlink(missing_ok=True)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from resume",
        )

    candidate_name, candidate_email = extract_candidate_details(
        extracted_text,
    )

    resume = Resume(
        user_id=current_user.id,
        job_id=job.id,
        original_filename=Path(file.filename).name,
        stored_filename=stored_filename,
        file_path=file_path,
        file_type=extension.lstrip("."),
        file_size=file_size,
        extracted_text=extracted_text,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
    )

    try:
        db.add(resume)
        db.commit()
        db.refresh(resume)
    except Exception:
        db.rollback()
        Path(file_path).unlink(missing_ok=True)
        raise

    return resume


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    file_path = Path(resume.file_path)

    db.delete(resume)
    db.commit()

    file_path.unlink(missing_ok=True)

    return None