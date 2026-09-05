from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = Job(
        recruiter_id=current_user.id,
        title=job_data.title,
        description=job_data.description,
        required_skills=job_data.required_skills,
        min_experience=job_data.min_experience,
        education=job_data.education,
        keywords=job_data.keywords,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Job)
        .filter(Job.recruiter_id == current_user.id)
        .order_by(Job.created_at.desc())
        .all()
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
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

    return job


@router.patch(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
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

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
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

    db.delete(job)
    db.commit()

    return None