from app.db.database import SessionLocal
from app.models.user import User


def test_create_and_read_user():
    db = SessionLocal()

    try:
        user = User(
            email="test@example.com",
            hashed_password="hashed-password",
            full_name="Test User",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"

        saved_user = (
            db.query(User)
            .filter(User.email == "test@example.com")
            .first()
        )

        assert saved_user is not None
        assert saved_user.id == user.id

    finally:
        db.query(User).filter(User.email == "test@example.com").delete()
        db.commit()
        db.close()