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

### Frontend

- **React.js** — Build the interactive web interface
- **Vite** — Fast frontend development and build tooling
- **HTML5 & CSS3** — Structure and styling
- **JavaScript / TypeScript** — Frontend logic
- **Tailwind CSS** — Responsive and modern UI design

### Backend

- **Python 3.12+** — Primary backend language
- **FastAPI** — REST API framework
- **Pydantic** — Data validation and serialization
- **SQLAlchemy** — Database ORM
- **Alembic** — Database migrations
- **Uvicorn** — ASGI server

### Database

- **PostgreSQL** — Primary relational database
- **Redis** — Caching and background-task support

### AI / Machine Learning

- **LLM API** — AI-powered study planning and recommendations
- **Python AI/ML libraries** — Future recommendation and analytics features

### Authentication & Security

- **JWT** — User authentication
- **OAuth2** — Authentication flow
- **PassLib / bcrypt** — Password hashing
- **Environment Variables (.env)** — Secure configuration management

### Testing & Code Quality

- **Pytest** — Backend testing
- **Ruff** — Python linting
- **Black** — Code formatting
- **MyPy** — Static type checking

### DevOps & Tools

- **Git & GitHub** — Version control and collaboration
- **Docker & Docker Compose** — Containerization
- **GitHub Actions** — CI/CD
- **Postman** — API testing and development

### Architecture

- **RESTful API Architecture**
- **Layered Backend Architecture**
- **Frontend–Backend Separation**
- **Database-driven application design**
