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

## Table of Contents

- [Overview](#overview)
- [Features](#features)
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
- [Docker Setup](#docker-setup)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

Resume Screening System is a full-stack recruitment platform designed to automate the initial resume screening process.

Recruiters can create job openings, upload candidate resumes, and automatically evaluate candidates based on job-specific requirements such as:

- Required skills
- Years of experience
- Education
- Relevant keywords

The system extracts text from uploaded PDF and DOCX resumes, analyzes the extracted content, calculates a weighted screening score, ranks candidates, and provides an explanation for the screening decision.

The goal is to reduce manual resume screening effort and provide recruiters with a structured and transparent way to compare candidates.

---

## Features

### 👤 Recruiter

- 🔐 Recruiter registration and login
- 🔑 JWT-based authentication
- 👤 Recruiter profile information
- 💼 Create job openings
- ✏️ Update job requirements
- 🗑️ Delete job openings
- 📋 View recruiter-owned jobs
- 📄 Upload candidate resumes
- 🗑️ Delete uploaded resumes
- 📊 View candidate rankings
- 🔎 View detailed candidate screening results
- 📈 View job-level screening statistics

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
- Secure recruiter ownership checks

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

Candidates are automatically:

- Scored
- Sorted by total score
- Assigned a ranking
- Classified as shortlisted or rejected
- Displayed in the recruiter dashboard

The ranking system makes it easy for recruiters to identify the strongest candidates.

### 💡 Screening Explanations

Every screening result includes explanations for:

- Skills match
- Experience match
- Education match
- Keyword match
- Overall recommendation

This makes the screening process more transparent instead of showing only a numerical score.

### 📊 Recruiter Dashboard

The dashboard provides:

- Total jobs
- Total candidates
- Screened resumes
- Shortlisted candidates
- Average candidate score
- Candidate ranking
- Candidate details
- Screening explanations
- Resume management

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
git clone https://github.com/Sayan1286/StudyPilot.git
cd StudyPilot
```

### 2. Set Up the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Copy environment file
copy .env.example .env
```

Edit `backend/.env` and configure the required environment variables.

### 3. Set Up the Database

Make sure PostgreSQL is running and the `studypilot` database has been created.

```bash
# Run database migrations
alembic upgrade head
```

### 4. Start the Backend

```bash
# Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

The backend will be available at http://localhost:8000.

Interactive API docs at http://localhost:8000/docs.

### 5. Set Up the Frontend

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install
```

### 6. Start the Frontend

```bash
# Start the Vite development server
npm run dev
```

The frontend will be available at http://localhost:5173.

### 7. Run Backend Tests

From the `backend` directory:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

### 8. Run Code Quality Checks

From the `backend` directory:

```bash
# Linting
ruff check .

# Code formatting
black .

# Static type checking
mypy .
```

### 9. Local Development URLs

| Service | URL |
|---|---|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **Interactive API Docs** | http://localhost:8000/docs |
| **PostgreSQL** | localhost:5432 |
