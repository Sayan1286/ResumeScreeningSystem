# Resume Screening System 📄
> **AI-powered resume screening and candidate ranking platform — helping recruiters discover the most relevant candidates faster and more efficiently.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)](https://alembic.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌐 Live Demo

### Frontend

https://resumescreeningsystem-1-qnrg.onrender.com

### Backend API

https://resumescreeningsystem-wpxz.onrender.com

### Interactive API Documentation

https://resumescreeningsystem-wpxz.onrender.com/docs

> **Note:** This project is currently deployed as an MVP for demonstration and testing purposes.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo Jobs](#demo-jobs)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Folder Structure](#folder-structure)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Environment Variables](#environment-variables)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Resume Screening](#resume-screening)
- [Candidate Ranking](#candidate-ranking)
- [Testing](#testing)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

Resume Screening System is a full-stack recruitment platform designed to simplify and automate the initial resume screening process.

Recruiters can create job openings, upload candidate resumes, and evaluate candidates based on job-specific requirements such as:

- Required skills
- Years of experience
- Education
- Relevant keywords

The system extracts text from uploaded PDF and DOCX resumes, analyzes the extracted content, calculates a weighted screening score, ranks candidates, and provides explanations for the screening decision.

The goal is to reduce manual resume screening effort and provide recruiters with a structured way to compare candidates.

---

## Features

### 👤 Authentication & Recruiter Management

- 🔐 Recruiter registration
- 🔑 JWT-based authentication
- 👤 Recruiter account management
- 🔒 Secure password hashing
- 📧 Password reset through email
- 🔗 Token-based password reset links

### 💼 Job Management

- ➕ Create job openings
- ✏️ Update recruiter-owned jobs
- 🗑️ Delete recruiter-owned jobs
- 📋 View available jobs
- 🔎 View job details
- 🔐 Recruiter ownership checks

### 🎯 Shared Demo Jobs

The system includes **10 permanent Demo Jobs** that are available to registered users.

Demo Jobs include:

- Junior Data Analyst
- Python Backend Developer
- Frontend Developer
- Full Stack Developer
- Software Engineer
- Machine Learning Engineer
- Data Scientist
- DevOps Engineer
- QA / Software Tester
- UI/UX Designer

Demo Jobs:

- ✅ Are available to all users
- ✅ Cannot be edited
- ✅ Cannot be deleted
- ✅ Are shared across users
- ✅ Keep user resume/screening data isolated

### 📄 Resume Management

- Upload PDF resumes
- Upload DOCX resumes
- File type validation
- File size validation
- Unique resume file storage
- Automatic resume text extraction
- Candidate name extraction
- Candidate email extraction
- Resume metadata storage
- Secure ownership checks

### 🤖 Resume Screening

Candidates are evaluated using a weighted scoring system:

| Category | Weight |
|----------|-------:|
| Skills | 40% |
| Experience | 25% |
| Education | 15% |
| Keywords | 20% |
| **Total** | **100%** |

The screening engine analyzes the extracted resume text against the requirements of the selected job.

### 🏆 Candidate Ranking

Candidates can be:

- Scored
- Sorted by total score
- Ranked
- Classified according to screening results
- Reviewed through detailed screening information

### 💡 Screening Explanations

Screening results provide explanations for:

- Skills match
- Experience match
- Education match
- Keyword match
- Overall screening result

This makes the screening process more transparent than showing only a numerical score.

### 📊 Dashboard

The recruiter dashboard provides access to:

- Job listings
- Candidate resumes
- Screening results
- Candidate rankings
- Job information
- Resume management
- Screening details

---


## Technology Stack

| Category | Technology | Version |
|---|---|---|
| **Frontend Framework** | React | 19.x |
| **Language (FE)** | TypeScript | 5.5+ |
| **Build Tool** | Vite | 5.x |
| **Styling** | Tailwind CSS | 3.4 |
| **Routing** | React Router | 6.x |
| **Data Fetching** | TanStack Query (React Query) | 5.x |
| **HTTP Client** | Axios | 1.7+ |
| **Forms** | React Hook Form + Zod | 7.x / 3.x |
| **Animations** | Framer Motion | 11.x |
| **Icons** | Lucide React | 0.424+ |
| **Backend Framework** | FastAPI | 0.115+ |
| **Language (BE)** | Python | 3.12+ |
| **Database** | PostgreSQL | 18.x |
| **ORM** | SQLAlchemy | 2.0+ |
| **Migrations** | Alembic | 1.19+ |
| **Validation** | Pydantic | v2 |
| **Authentication** | JWT / OAuth2 | — |
| **Password Hashing** | PassLib / bcrypt | — |
| **Caching** | Redis | 7.x+ |
| **AI / LLM** | LLM API | — |
| **AI Libraries** | Python AI/ML Libraries | — |
| **Testing** | Pytest | Latest |
| **Linting** | Ruff | Latest |
| **Formatting** | Black | Latest |
| **Type Checking** | MyPy | Latest |
| **Containerization** | Docker | Latest |
| **Orchestration** | Docker Compose | Latest |
| **CI/CD** | GitHub Actions | — |
| **API Testing** | Postman | Latest |
| **Version Control** | Git / GitHub | — |

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/Sayan1286/ResumeScreeningSystem.git
cd ResumeScreeningSystem
```

### 2. Set Up the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Configure Environment Variables
Create a .env file inside the backend directory.

DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/resume_screening
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
RESEND_API_KEY=your-resend-api-key
MAIL_FROM=onboarding@resend.dev
FRONTEND_URL=http://localhost:5173

### 3. Set Up the Database
  Make sure PostgreSQL is running and create the project database.

```bash
# Run database migrations
alembic upgrade head
``` This applies all database migrations, including the Demo Jobs.

### 4. Start the Backend

```bash
# Running the Backend
python -m uvicorn app.main:app --reload
```

The backend will be available at http://127.0.0.1:8000

### 5. Set Up the Frontend

Open a **new terminal**:

```bash
cd frontend

# Install frontend dependencies:
npm install
```

### 6. Start the Frontend

```bash
# Start the Vite development server
npm run dev
```

The frontend will be available at http://localhost:5173.

### 7.Database Setup

The application uses PostgreSQL for persistent data storage.

Alembic manages database migrations.

 Run migrations:
```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```
View migration history:
```bash
alembic history
```
### 8.Environment Variables

Backend

Variable	Description
DATABASE_URL	PostgreSQL database connection URL
JWT_SECRET_KEY	Secret used for JWT authentication
JWT_ALGORITHM	JWT signing algorithm
RESEND_API_KEY	Resend API key for password reset emails
MAIL_FROM	Email sender address
FRONTEND_URL	Frontend URL used for password reset links

Frontend

The deployed frontend is configured to communicate with the deployed FastAPI backend.

### 9. API Documentation

When the backend is running locally:
 http://127.0.0.1:8000/docs

The deployed API documentation is available at:
https://resumescreeningsystem-wpxz.onrender.com/docs

The API documentation is generated automatically using FastAPI and OpenAPI.

### 10. Resume Screening

The screening workflow is:

Upload Resume
      ↓
Extract Resume Text
      ↓
Read Job Requirements
      ↓
Match Skills
      ↓
Match Experience
      ↓
Match Education
      ↓
Match Keywords
      ↓
Calculate Score
      ↓
Generate Screening Result
### 11.Candidate Ranking

Candidates are evaluated using their screening scores.

Higher matching scores indicate stronger alignment with the selected job requirements.

The system allows recruiters to review:

Candidate information
Resume information
Screening score
Category-level results
Screening explanation

### 12.Testing
From the backend directory:
```bash
pytest
```
Run tests with verbose output:
```bash
pytest -v
```
Run a specific test file:
```bash
pytest tests/test_jobs.py
```
### 13.Code Quality
Ruff :

```bash
ruff check .
```
MyPy:
```bash
mypy .
```
Git Diff Check
```bash
git diff --check
```
### 14.Deployment

The current MVP is deployed using Render.
Frontend
https://resumescreeningsystem-1-qnrg.onrender.com

Backend
https://resumescreeningsystem-wpxz.onrender.com

API Documentation
https://resumescreeningsystem-wpxz.onrender.com/docs

Email Service
Password reset emails are sent using Resend.

### 15.Screenshots

Add application screenshots here.

![Login Page](docs/screenshots/login.png)

![Dashboard](docs/screenshots/dashboard.png)

![Job Listings](docs/screenshots/jobs.png)

![Candidate Screening](docs/screenshots/screening.png)

### 16.Security Notes

The application includes:

JWT authentication
Password hashing
Token-based password reset
Resume ownership checks
Job ownership checks
File validation
Protected API endpoints
Environment-based secret configuration

Production deployments should use secure secrets and properly configured domain/email settings.

### 17.License

This project is licensed under the MIT License.

See the LICENSE file for details.

### 17.Contact

Sayan Das

GitHub:
https://github.com/Sayan1286

Repository:
https://github.com/Sayan1286/ResumeScreeningSystem
