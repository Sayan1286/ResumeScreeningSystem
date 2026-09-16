
"""add demo job

Revision ID: 8d1a5d303419
Revises: 097b6c5d3949
Create Date: 2026-09-15
"""

from alembic import op
import sqlalchemy as sa


revision = "8d1a5d303419"
down_revision = "097b6c5d3949"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "jobs",
        "recruiter_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.add_column(
        "jobs",
        sa.Column(
            "is_demo",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_index(
        "ix_jobs_is_demo",
        "jobs",
        ["is_demo"],
        unique=False,
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

    op.execute(
        jobs_table.insert().values(
            recruiter_id=None,
            is_demo=True,
            title="Junior Data Analyst",
            description=(
                "Demo job for testing the Resume Screening System. "
                "Candidates should have basic data analysis skills "
                "and familiarity with databases and spreadsheets."
            ),
            required_skills="Python, SQL, Excel, Data Analysis",
            min_experience=0,
            education="B.Tech / B.Sc / Any relevant degree",
            keywords="Data Analysis, SQL, Python, Excel, Database",
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM jobs WHERE is_demo = TRUE"
        )
    )

    op.drop_index(
        "ix_jobs_is_demo",
        table_name="jobs",
    )

    op.drop_column(
        "jobs",
        "is_demo",
    )

    op.alter_column(
        "jobs",
        "recruiter_id",
        existing_type=sa.Integer(),
        nullable=False,
    )