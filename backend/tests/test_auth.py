import uuid

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.main import app
from app.models.user import User


client = TestClient(app)


def create_test_email() -> str:
    return f"test-{uuid.uuid4().hex}@example.com"


def cleanup_user(email: str) -> None:
    db = SessionLocal()

    try:
        db.query(User).filter(User.email == email).delete()
        db.commit()
    finally:
        db.close()


def test_register_user():
    email = create_test_email()

    try:
        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Test User",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

    finally:
        cleanup_user(email)


def test_register_duplicate_email():
    email = create_test_email()

    try:
        first_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Test User",
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Another User",
            },
        )

        assert second_response.status_code == 409
        assert second_response.json()["detail"] == "Email already registered"

    finally:
        cleanup_user(email)


def test_login_success():
    email = create_test_email()

    try:
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Test User",
            },
        )

        assert register_response.status_code == 201

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "TestPassword123",
            },
        )

        assert login_response.status_code == 200

        data = login_response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

    finally:
        cleanup_user(email)


def test_login_wrong_password():
    email = create_test_email()

    try:
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Test User",
            },
        )

        assert register_response.status_code == 201

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "WrongPassword123",
            },
        )

        assert login_response.status_code == 401
        assert login_response.json()["detail"] == "Invalid email or password"

    finally:
        cleanup_user(email)


def test_login_unknown_email():
    email = create_test_email()

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_get_current_user():
    email = create_test_email()

    try:
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "TestPassword123",
                "full_name": "Test User",
            },
        )

        assert register_response.status_code == 201

        token = register_response.json()["access_token"]

        response = client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["email"] == email
        assert data["full_name"] == "Test User"
        assert "id" in data
        assert "created_at" in data

    finally:
        cleanup_user(email)


def test_get_current_user_with_invalid_token():
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"