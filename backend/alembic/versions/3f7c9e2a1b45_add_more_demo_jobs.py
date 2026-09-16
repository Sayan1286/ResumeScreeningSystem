"""replace single demo job with ten demo jobs

Revision ID: 3f7c9e2a1b45
Revises: 8d1a5d303419
Create Date: 2026-09-16
"""

from alembic import op
import sqlalchemy as sa


revision = "3f7c9e2a1b45"
down_revision = "8d1a5d303419"
branch_labels = None
depends_on = None


def upgrade() -> None:
    jobs_table = sa.table(
        "jobs",
        sa.column("id", sa.Integer()),
        sa.column("recruiter_id", sa.Integer()),
        sa.column("is_demo", sa.Boolean()),
        sa.column("title", sa.String()),
        sa.column("description", sa.Text()),
        sa.column("required_skills", sa.Text()),
        sa.column("min_experience", sa.Integer()),
        sa.column("education", sa.String()),
        sa.column("keywords", sa.Text()),
    )

    # Remove the existing single demo job.
    op.execute(
        sa.text(
            "DELETE FROM jobs WHERE is_demo = TRUE"
        )
    )

    # Insert ten shared demo jobs.
    demo_jobs = [
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Junior Data Analyst",
            "description": (
                "Entry-level data analyst role focused on "
                "data cleaning, reporting, dashboards, and "
                "basic statistical analysis."
            ),
            "required_skills": "Python, SQL, Excel, Data Analysis",
            "min_experience": 0,
            "education": "B.Tech / B.Sc / Any relevant degree",
            "keywords": (
                "Data Analysis, SQL, Python, Excel, "
                "Database, Reporting"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Python Backend Developer",
            "description": (
                "Backend development role involving Python "
                "APIs, databases, authentication, and "
                "server-side application development."
            ),
            "required_skills": (
                "Python, FastAPI, Django, SQL, REST API"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / BCA / MCA / Any relevant degree"
            ),
            "keywords": (
                "Python, FastAPI, Django, Backend, REST API, "
                "SQL, PostgreSQL, Git"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Frontend Developer",
            "description": (
                "Frontend development role focused on "
                "building responsive and interactive web "
                "applications."
            ),
            "required_skills": (
                "React, TypeScript, JavaScript, HTML, CSS"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / BCA / MCA / Any relevant degree"
            ),
            "keywords": (
                "React, TypeScript, JavaScript, HTML, CSS, "
                "Frontend, Vite, Git"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Full Stack Developer",
            "description": (
                "Full stack role involving frontend and "
                "backend application development, APIs, "
                "databases, and deployment."
            ),
            "required_skills": (
                "React, TypeScript, Python, Node.js, SQL"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / BCA / MCA / Any relevant degree"
            ),
            "keywords": (
                "React, TypeScript, Python, Node.js, "
                "SQL, REST API, Git, Full Stack"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Software Engineer",
            "description": (
                "Software engineering role focused on "
                "developing reliable applications, solving "
                "technical problems, and maintaining code."
            ),
            "required_skills": (
                "Python, Java, C++, Git, Algorithms"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / B.E. / BCA / MCA / Any relevant degree"
            ),
            "keywords": (
                "Software Engineering, Python, Java, C++, "
                "Algorithms, Data Structures, Git"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Machine Learning Engineer",
            "description": (
                "Machine learning role involving model "
                "development, data preparation, evaluation, "
                "and deployment of ML solutions."
            ),
            "required_skills": (
                "Python, Machine Learning, "
                "Scikit-learn, TensorFlow, SQL"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / B.Sc / M.Tech / MCA / Any relevant degree"
            ),
            "keywords": (
                "Machine Learning, Python, Scikit-learn, "
                "TensorFlow, Pandas, NumPy, SQL"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "Data Scientist",
            "description": (
                "Data science role focused on analyzing "
                "complex datasets, building predictive "
                "models, and communicating insights."
            ),
            "required_skills": (
                "Python, Pandas, NumPy, SQL, Machine Learning"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / B.Sc / M.Tech / M.Sc / Any relevant degree"
            ),
            "keywords": (
                "Data Science, Python, Pandas, NumPy, "
                "SQL, Machine Learning, Statistics"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "DevOps Engineer",
            "description": (
                "DevOps role focused on automation, "
                "containerization, CI/CD pipelines, "
                "cloud infrastructure, and system reliability."
            ),
            "required_skills": (
                "Docker, Linux, AWS, CI/CD, Kubernetes"
            ),
            "min_experience": 1,
            "education": (
                "B.Tech / B.E. / MCA / Any relevant degree"
            ),
            "keywords": (
                "DevOps, Docker, Linux, AWS, CI/CD, "
                "Kubernetes, Git, Cloud"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "QA / Software Tester",
            "description": (
                "Quality assurance role involving manual "
                "and automated testing, API testing, "
                "bug reporting, and test case development."
            ),
            "required_skills": (
                "Selenium, Python, API Testing, SQL, Testing"
            ),
            "min_experience": 0,
            "education": (
                "B.Tech / BCA / MCA / Any relevant degree"
            ),
            "keywords": (
                "QA, Testing, Selenium, Python, "
                "API Testing, SQL, Automation"
            ),
        },
        {
            "recruiter_id": None,
            "is_demo": True,
            "title": "UI/UX Designer",
            "description": (
                "UI/UX design role focused on user research, "
                "wireframes, prototypes, visual design, "
                "and creating user-friendly digital products."
            ),
            "required_skills": (
                "Figma, UI Design, UX, Prototyping, Wireframing"
            ),
            "min_experience": 0,
            "education": (
                "Any relevant degree / Design qualification"
            ),
            "keywords": (
                "UI Design, UX Design, Figma, "
                "Prototyping, Wireframing, User Research"
            ),
        },
    ]

    op.bulk_insert(jobs_table, demo_jobs)


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM jobs WHERE is_demo = TRUE"
        )
    )

    jobs_table = sa.table(
        "jobs",
        sa.column("recruiter_id", sa.Integer()),
        sa.column("is_demo", sa.Boolean()),
        sa.column("title", sa.String()),
        sa.column("description", sa.Text()),
        sa.column("required_skills", sa.Text()),
        sa.column("min_experience", sa.Integer()),
        sa.column("education", sa.String()),
        sa.column("keywords", sa.Text()),
    )

    op.bulk_insert(
        jobs_table,
        [
            {
                "recruiter_id": None,
                "is_demo": True,
                "title": "Junior Data Analyst",
                "description": (
                    "Demo job for testing the Resume Screening System."
                ),
                "required_skills": (
                    "Python, SQL, Excel, Data Analysis"
                ),
                "min_experience": 0,
                "education": (
                    "B.Tech / B.Sc / Any relevant degree"
                ),
                "keywords": (
                    "Data Analysis, SQL, Python, Excel, Database"
                ),
            }
        ],
    )