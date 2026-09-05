from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.schemas.screening import ScreeningResult
from app.services.screening import calculate_screening_score


router = APIRouter(
    prefix="/screening",
    tags=["Screening"],
)


@router.get(
    "/jobs/{job_id}",
    response_model=list[ScreeningResult],
)
def screen_job_candidates(
    job_id: int,
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

    resumes = (
        db.query(Resume)
        .join(User, Resume.user_id == User.id)
        .filter(Resume.job_id == job.id)
        .all()
    )

    results = []

    for resume in resumes:
        score = calculate_screening_score(
            resume_text=resume.extracted_text or "",
            required_skills=job.required_skills,
            min_experience=job.min_experience,
            education=job.education,
            keywords=job.keywords,
        )

        results.append(
            ScreeningResult(
                resume_id=resume.id,
                candidate_id=resume.user_id,
                candidate_name=resume.user.full_name,
                candidate_email=resume.user.email,
                original_filename=resume.original_filename,
                **score,
            )
        )

    results.sort(
        key=lambda result: result.total_score,
        reverse=True,
    )

    return results