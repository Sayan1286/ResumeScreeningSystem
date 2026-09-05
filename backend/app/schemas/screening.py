from pydantic import BaseModel


class ScreeningResult(BaseModel):
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