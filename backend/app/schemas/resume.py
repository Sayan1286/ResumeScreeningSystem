from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    extracted_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )