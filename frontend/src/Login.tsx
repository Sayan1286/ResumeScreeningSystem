import { useState } from "react";
import type { FormEvent } from "react";

type LoginProps = {
  onLogin: (token: string) => void;
};

type Mode = "login" | "register" | "forgot" | "reset";

const API_BASE_URL = "https://resumescreeningsystem-wpxz.onrender.com";;

export default function Login({ onLogin }: LoginProps) {
  const resetToken = new URLSearchParams(window.location.search).get(
    "reset_token",
  );

  const [mode, setMode] = useState<Mode>(
    resetToken ? "reset" : "login",
  );

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Password visibility
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const clearMessages = () => {
    setError("");
    setSuccess("");
  };

  const changeMode = (newMode: Mode) => {
    setMode(newMode);
    clearMessages();
  };

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      // =========================
      // LOGIN
      // =========================
      if (mode === "login") {
        const response = await fetch(
          `${API_BASE_URL}/auth/login`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email,
              password,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Login failed");
        }

        localStorage.setItem(
          "access_token",
          data.access_token,
        );

        onLogin(data.access_token);
        return;
      }

      // =========================
      // REGISTER
      // =========================
      if (mode === "register") {
        const response = await fetch(
          `${API_BASE_URL}/auth/register`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email,
              password,
              full_name: fullName,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Registration failed",
          );
        }

        localStorage.setItem(
          "access_token",
          data.access_token,
        );

        onLogin(data.access_token);
        return;
      }

      // =========================
      // FORGOT PASSWORD
      // =========================
      if (mode === "forgot") {
        const response = await fetch(
          `${API_BASE_URL}/auth/forgot-password`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to send password reset email",
          );
        }

        setSuccess(
          "If an account with that email exists, a password reset link has been sent.",
        );

        return;
      }

      // =========================
      // RESET PASSWORD
      // =========================
      if (mode === "reset") {
        if (!resetToken) {
          throw new Error(
            "Invalid or missing reset token.",
          );
        }

        if (newPassword !== confirmPassword) {
          throw new Error(
            "Passwords do not match.",
          );
        }

        const response = await fetch(
          `${API_BASE_URL}/auth/reset-password`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              token: resetToken,
              new_password: newPassword,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail ||
              "Unable to reset password",
          );
        }

        setSuccess(
          "Password reset successfully. You can now log in.",
        );

        setNewPassword("");
        setConfirmPassword("");

        setShowNewPassword(false);
        setShowConfirmPassword(false);

        // Remove reset token from browser URL
        window.history.replaceState(
          {},
          document.title,
          window.location.pathname,
        );

        setMode("login");
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong",
      );
    } finally {
      setLoading(false);
    }
  }

  const getTitle = () => {
    if (mode === "register") {
      return "Create your account";
    }

    if (mode === "forgot") {
      return "Forgot password?";
    }

    if (mode === "reset") {
      return "Reset your password";
    }

    return "Welcome back";
  };

  const getSubtitle = () => {
    if (mode === "register") {
      return "Create an account to start screening resumes.";
    }

    if (mode === "forgot") {
      return "Enter your email and we'll send you a reset link.";
    }

    if (mode === "reset") {
      return "Create a new password for your account.";
    }

    return "Sign in to your Resume Screening System.";
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <h1>{getTitle()}</h1>
          <p>{getSubtitle()}</p>
        </div>

        {/* ERROR */}
        {error && (
          <div className="login-error">
            {error}
          </div>
        )}

        {/* SUCCESS */}
        {success && (
          <div className="login-success">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* =========================
              FULL NAME
          ========================= */}
          {mode === "register" && (
            <div className="login-field">
              <label htmlFor="fullName">
                Full name
              </label>

              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(event) =>
                  setFullName(event.target.value)
                }
                placeholder="Enter your full name"
                required
                minLength={1}
                maxLength={255}
              />
            </div>
          )}

          {/* =========================
              EMAIL
          ========================= */}
          {(mode === "login" ||
            mode === "register" ||
            mode === "forgot") && (
            <div className="login-field">
              <label htmlFor="email">
                Email
              </label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="Enter your email"
                required
              />
            </div>
          )}

          {/* =========================
              LOGIN PASSWORD
          ========================= */}
          {mode === "login" && (
            <div className="login-field">
              <label htmlFor="loginPassword">
                Password
              </label>

              <div className="password-input-wrapper">
                <input
                  id="loginPassword"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  placeholder="Enter your password"
                  required
                  minLength={8}
                  maxLength={128}
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(
                      !showPassword,
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                  title={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "🙈" : "👁️"}
                </button>
              </div>
            </div>
          )}

          {/* =========================
              REGISTER PASSWORD
          ========================= */}
          {mode === "register" && (
            <div className="login-field">
              <label htmlFor="registerPassword">
                Password
              </label>

              <div className="password-input-wrapper">
                <input
                  id="registerPassword"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  placeholder="Create a password"
                  required
                  minLength={8}
                  maxLength={128}
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(
                      !showPassword,
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                  title={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "🙈" : "👁️"}
                </button>
              </div>

              <small className="password-hint">
                Password must be 8–128 characters.
              </small>
            </div>
          )}

          {/* =========================
              RESET PASSWORD
          ========================= */}
          {mode === "reset" && (
            <>
              {/* NEW PASSWORD */}
              <div className="login-field">
                <label htmlFor="newPassword">
                  New password
                </label>

                <div className="password-input-wrapper">
                  <input
                    id="newPassword"
                    type={
                      showNewPassword
                        ? "text"
                        : "password"
                    }
                    value={newPassword}
                    onChange={(event) =>
                      setNewPassword(
                        event.target.value,
                      )
                    }
                    placeholder="Enter new password"
                    required
                    minLength={8}
                    maxLength={128}
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowNewPassword(
                        !showNewPassword,
                      )
                    }
                    aria-label={
                      showNewPassword
                        ? "Hide password"
                        : "Show password"
                    }
                    title={
                      showNewPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showNewPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>
              </div>

              {/* CONFIRM PASSWORD */}
              <div className="login-field">
                <label htmlFor="confirmPassword">
                  Confirm password
                </label>

                <div className="password-input-wrapper">
                  <input
                    id="confirmPassword"
                    type={
                      showConfirmPassword
                        ? "text"
                        : "password"
                    }
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(
                        event.target.value,
                      )
                    }
                    placeholder="Confirm new password"
                    required
                    minLength={8}
                    maxLength={128}
                  />

                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowConfirmPassword(
                        !showConfirmPassword,
                      )
                    }
                    aria-label={
                      showConfirmPassword
                        ? "Hide password"
                        : "Show password"
                    }
                    title={
                      showConfirmPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showConfirmPassword
                      ? "🙈"
                      : "👁️"}
                  </button>
                </div>
              </div>
            </>
          )}

          {/* =========================
              FORGOT PASSWORD BUTTON
          ========================= */}
          {mode === "login" && (
            <button
              type="button"
              className="forgot-password-button"
              onClick={() =>
                changeMode("forgot")
              }
            >
              Forgot password?
            </button>
          )}

          {/* =========================
              SUBMIT BUTTON
          ========================= */}
          <button
            type="submit"
            className="login-submit"
            disabled={loading}
          >
            {loading
              ? "Please wait..."
              : mode === "login"
                ? "Login"
                : mode === "register"
                  ? "Create account"
                  : mode === "forgot"
                    ? "Send reset link"
                    : "Reset password"}
          </button>
        </form>

        {/* =========================
            LOGIN → REGISTER
        ========================= */}
        {mode === "login" && (
          <div className="auth-switch">
            Don't have an account?{" "}
            <button
              type="button"
              onClick={() =>
                changeMode("register")
              }
            >
              Register
            </button>
          </div>
        )}

        {/* =========================
            REGISTER → LOGIN
        ========================= */}
        {mode === "register" && (
          <div className="auth-switch">
            Already have an account?{" "}
            <button
              type="button"
              onClick={() =>
                changeMode("login")
              }
            >
              Login
            </button>
          </div>
        )}

        {/* =========================
            FORGOT → LOGIN
        ========================= */}
        {mode === "forgot" && (
          <div className="auth-switch">
            Remember your password?{" "}
            <button
              type="button"
              onClick={() =>
                changeMode("login")
              }
            >
              Back to login
            </button>
          </div>
        )}

        {/* =========================
            RESET → LOGIN
        ========================= */}
        {mode === "reset" && (
          <div className="auth-switch">
            Remember your password?{" "}
            <button
              type="button"
              onClick={() =>
                changeMode("login")
              }
            >
              Back to login
            </button>
          </div>
        )}
      </div>
    </div>
  );
}