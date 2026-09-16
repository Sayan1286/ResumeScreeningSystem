import resend

from app.core.config import settings


def send_password_reset_email(
    to_email: str,
    reset_url: str,
) -> None:
    """Send a password reset email using Resend."""

    if not settings.resend_api_key:
        raise RuntimeError("RESEND_API_KEY is not configured")

    resend.api_key = settings.resend_api_key

    params = {
        "from": settings.mail_from,
        "to": [to_email],
        "subject": "Reset your Resume Screening System password",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2>Password Reset</h2>

            <p>
                We received a request to reset your password.
            </p>

            <p>
                Click the button below to create a new password:
            </p>

            <p>
                <a
                    href="{reset_url}"
                    style="
                        display: inline-block;
                        padding: 12px 20px;
                        background: #2563eb;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                    "
                >
                    Reset Password
                </a>
            </p>

            <p>
                This link will expire in 30 minutes.
            </p>

            <p>
                If you did not request a password reset, you can safely
                ignore this email.
            </p>

            <p>
                Resume Screening System
            </p>
        </div>
        """,
    }

    resend.Emails.send(params)