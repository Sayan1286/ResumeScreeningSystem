from pydantic import BaseModel


class ScreeningResult(BaseModel):
    rank: int
    resume_id: int
    candidate_id: int
    candidate_name: str
    candidate_email: str
    original_filename: str

    skill_score: float
    experience_score: float
    education_score: float
    keyword_score: float
    total_score: float

    match_percentage: float
    status: str

    skills_explanation: str
    experience_explanation: str
    education_explanation: str
    keywords_explanation: str
    recommendation: str