from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str = Field(
        min_length=1,
    )

    required_skills: str = Field(
        min_length=1,
    )

    min_experience: int = Field(
        default=0,
        ge=0,
    )

    education: str | None = Field(
        default=None,
        max_length=255,
    )

    keywords: str | None = None


class JobUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
    )

    required_skills: str | None = Field(
        default=None,
        min_length=1,
    )

    min_experience: int | None = Field(
        default=None,
        ge=0,
    )

    education: str | None = Field(
        default=None,
        max_length=255,
    )

    keywords: str | None = None


class JobResponse(BaseModel):
    id: int
    recruiter_id: int
    title: str
    description: str
    required_skills: str
    min_experience: int
    education: str | None
    keywords: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )