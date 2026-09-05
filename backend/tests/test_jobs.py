import uuid

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.main import app
from app.models.job import Job
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


def cleanup_user(email: str) -> None:
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user:
            db.query(Job).filter(
                Job.recruiter_id == user.id
            ).delete()

            db.delete(user)
            db.commit()

    finally:
        db.close()


def job_payload(title: str = "Backend Engineer") -> dict:
    return {
        "title": title,
        "description": "Build and maintain backend APIs.",
        "required_skills": "Python, FastAPI, PostgreSQL",
        "min_experience": 2,
        "education": "B.Tech Computer Science",
        "keywords": "FastAPI, SQLAlchemy, REST API",
    }


def test_create_job():
    email, token = create_test_user()

    try:
        response = client.post(
            "/jobs",
            json=job_payload(),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["title"] == "Backend Engineer"
        assert data["description"] == "Build and maintain backend APIs."
        assert data["required_skills"] == "Python, FastAPI, PostgreSQL"
        assert data["min_experience"] == 2
        assert data["education"] == "B.Tech Computer Science"
        assert data["keywords"] == "FastAPI, SQLAlchemy, REST API"
        assert data["recruiter_id"] is not None
        assert data["id"] is not None
        assert "created_at" in data
        assert "updated_at" in data

    finally:
        cleanup_user(email)


def test_list_jobs():
    email, token = create_test_user()

    try:
        first_response = client.post(
            "/jobs",
            json=job_payload("Backend Engineer"),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        second_response = client.post(
            "/jobs",
            json=job_payload("Python Developer"),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert first_response.status_code == 201
        assert second_response.status_code == 201

        response = client.get(
            "/jobs",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["title"] == "Python Developer"
        assert data[1]["title"] == "Backend Engineer"

    finally:
        cleanup_user(email)


def test_get_job():
    email, token = create_test_user()

    try:
        create_response = client.post(
            "/jobs",
            json=job_payload(),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert create_response.status_code == 201

        job_id = create_response.json()["id"]

        response = client.get(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200
        assert response.json()["id"] == job_id
        assert response.json()["title"] == "Backend Engineer"

    finally:
        cleanup_user(email)


def test_get_nonexistent_job():
    email, token = create_test_user()

    try:
        response = client.get(
            "/jobs/999999999",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    finally:
        cleanup_user(email)


def test_update_job():
    email, token = create_test_user()

    try:
        create_response = client.post(
            "/jobs",
            json=job_payload(),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert create_response.status_code == 201

        job_id = create_response.json()["id"]

        response = client.patch(
            f"/jobs/{job_id}",
            json={
                "title": "Senior Backend Engineer",
                "min_experience": 5,
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == job_id
        assert data["title"] == "Senior Backend Engineer"
        assert data["min_experience"] == 5
        assert data["description"] == "Build and maintain backend APIs."

    finally:
        cleanup_user(email)


def test_delete_job():
    email, token = create_test_user()

    try:
        create_response = client.post(
            "/jobs",
            json=job_payload(),
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert create_response.status_code == 201

        job_id = create_response.json()["id"]

        delete_response = client.delete(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert delete_response.status_code == 204

        get_response = client.get(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert get_response.status_code == 404

    finally:
        cleanup_user(email)


def test_user_cannot_access_another_users_job():
    owner_email, owner_token = create_test_user()
    other_email, other_token = create_test_user()

    try:
        create_response = client.post(
            "/jobs",
            json=job_payload(),
            headers={
                "Authorization": f"Bearer {owner_token}",
            },
        )

        assert create_response.status_code == 201

        job_id = create_response.json()["id"]

        get_response = client.get(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {other_token}",
            },
        )

        assert get_response.status_code == 404

        update_response = client.patch(
            f"/jobs/{job_id}",
            json={
                "title": "Unauthorized Update",
            },
            headers={
                "Authorization": f"Bearer {other_token}",
            },
        )

        assert update_response.status_code == 404

        delete_response = client.delete(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {other_token}",
            },
        )

        assert delete_response.status_code == 404

        owner_get_response = client.get(
            f"/jobs/{job_id}",
            headers={
                "Authorization": f"Bearer {owner_token}",
            },
        )

        assert owner_get_response.status_code == 200
        assert owner_get_response.json()["title"] == "Backend Engineer"

    finally:
        cleanup_user(owner_email)
        cleanup_user(other_email)


def test_jobs_require_authentication():
    response = client.get("/jobs")

    assert response.status_code in (401, 403)