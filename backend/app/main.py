from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(
    title="Resume Screening System",
    description="AI-powered resume screening and candidate ranking API",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "resume-screening-system",
    }