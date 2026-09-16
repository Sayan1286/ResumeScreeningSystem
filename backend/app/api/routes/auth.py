from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.email import send_password_reset_email
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def hash_reset_token(token: str) -> str:
    """Hash a password reset token before storing it in the database."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        subject=str(user.id),
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not user or not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        subject=str(user.id),
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post(
    "/forgot-password",
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    # Do not reveal whether an email address is registered.
    if not user:
        return {
            "message": (
                "If an account with that email exists, "
                "a password reset link has been sent."
            )
        }

    # Generate a secure random token.
    reset_token = secrets.token_urlsafe(32)

    # Store only the hash of the token in the database.
    user.reset_token = hash_reset_token(reset_token)

    # Token expires after 30 minutes.
    user.reset_token_expires_at = (
        datetime.now(timezone.utc) + timedelta(minutes=30)
    )

    db.commit()

    # Build the password reset URL.
    reset_url = (
        f"{settings.frontend_url}/"
        f"?reset_token={reset_token}"
    )

    try:
        send_password_reset_email(
            to_email=user.email,
            reset_url=reset_url,
        )
    except Exception as exc:
        # Invalidate the token if the email could not be sent.
        user.reset_token = None
        user.reset_token_expires_at = None
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to send password reset email",
        ) from exc

    return {
        "message": (
            "If an account with that email exists, "
            "a password reset link has been sent."
        )
    }


@router.post(
    "/reset-password",
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    # Hash the token received from the frontend.
    token_hash = hash_reset_token(request.token)

    user = (
        db.query(User)
        .filter(User.reset_token == token_hash)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    # Check whether the token has expired.
    if (
        not user.reset_token_expires_at
        or user.reset_token_expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    # Update the password.
    user.hashed_password = hash_password(
        request.new_password,
    )

    # Invalidate the reset token so it cannot be reused.
    user.reset_token = None
    user.reset_token_expires_at = None

    db.commit()

    return {
        "message": (
            "Password reset successfully. "
            "You can now log in."
        )
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user