import io
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.database import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User


client = TestClient(app)


def create_test_user() -> tuple[str, str]:
    email = f"recruiter-{uuid.uuid4().hex}@example.com"
    password = "TestPassword123"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Test Recruiter",
        },
    )

    assert response.status_code == 201

    return email, response.json()["access_token"]


def create_test_job(token: str) -> int:
    response = client.post(
        "/jobs",
        json={
            "title": "Backend Engineer",
            "description": "Build backend APIs.",
            "required_skills": "Python, FastAPI, PostgreSQL",
            "min_experience": 2,
            "education": "B.Tech",
            "keywords": "FastAPI, SQLAlchemy",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    return response.json()["id"]


def cleanup_user(email: str) -> None:
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user:
            resumes = (
                db.query(Resume)
                .filter(Resume.user_id == user.id)
                .all()
            )

            for resume in resumes:
                Path(resume.file_path).unlink(missing_ok=True)

            db.query(Resume).filter(
                Resume.user_id == user.id
            ).delete()

            db.query(Job).filter(
                Job.recruiter_id == user.id
            ).delete()

            db.delete(user)
            db.commit()

    finally:
        db.close()


def test_upload_pdf_resume():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.pdf",
                    io.BytesIO(b"%PDF-1.4 test resume"),
                    "application/pdf",
                )
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201

        data = response.json()

        assert data["original_filename"] == "resume.pdf"
        assert data["file_type"] == "pdf"
        assert data["file_size"] > 0
        assert data["job_id"] == job_id
        assert data["user_id"] is not None

        stored_path = Path(data["file_path"])

        assert stored_path.exists()
        assert stored_path.suffix == ".pdf"

    finally:
        cleanup_user(email)


def test_upload_docx_resume():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.docx",
                    io.BytesIO(b"fake docx content"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201

        data = response.json()

        assert data["original_filename"] == "resume.docx"
        assert data["file_type"] == "docx"

    finally:
        cleanup_user(email)


def test_reject_unsupported_resume_type():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.txt",
                    io.BytesIO(b"plain text"),
                    "text/plain",
                )
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Only PDF and DOCX files are allowed"
        )

    finally:
        cleanup_user(email)


def test_upload_requires_authentication():
    response = client.post(
        "/resumes?job_id=1",
        files={
            "file": (
                "resume.pdf",
                io.BytesIO(b"%PDF-1.4 test"),
                "application/pdf",
            )
        },
    )

    assert response.status_code in (401, 403)


def test_upload_to_another_users_job_is_rejected():
    owner_email, owner_token = create_test_user()
    other_email, other_token = create_test_user()

    try:
        job_id = create_test_job(owner_token)

        response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.pdf",
                    io.BytesIO(b"%PDF-1.4 test"),
                    "application/pdf",
                )
            },
            headers={"Authorization": f"Bearer {other_token}"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    finally:
        cleanup_user(owner_email)
        cleanup_user(other_email)


def test_list_resumes():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        for filename in ("first.pdf", "second.pdf"):
            response = client.post(
                f"/resumes?job_id={job_id}",
                files={
                    "file": (
                        filename,
                        io.BytesIO(b"%PDF-1.4 test"),
                        "application/pdf",
                    )
                },
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 201

        response = client.get(
            "/resumes",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert len(response.json()) == 2

    finally:
        cleanup_user(email)


def test_get_resume():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        upload_response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.pdf",
                    io.BytesIO(b"%PDF-1.4 test"),
                    "application/pdf",
                )
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        resume_id = upload_response.json()["id"]

        response = client.get(
            f"/resumes/{resume_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["id"] == resume_id

    finally:
        cleanup_user(email)


def test_get_nonexistent_resume():
    email, token = create_test_user()

    try:
        response = client.get(
            "/resumes/999999999",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Resume not found"

    finally:
        cleanup_user(email)


def test_delete_resume():
    email, token = create_test_user()

    try:
        job_id = create_test_job(token)

        upload_response = client.post(
            f"/resumes?job_id={job_id}",
            files={
                "file": (
                    "resume.pdf",
                    io.BytesIO(b"%PDF-1.4 test"),
                    "application/pdf",
                )
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert upload_response.status_code == 201

        data = upload_response.json()
        resume_id = data["id"]
        file_path = Path(data["file_path"])

        assert file_path.exists()

        response = client.delete(
            f"/resumes/{resume_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 204
        assert not file_path.exists()

        get_response = client.get(
            f"/resumes/{resume_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert get_response.status_code == 404

    finally:
        cleanup_user(email)