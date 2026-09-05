from app.services.screening import (
    EDUCATION_WEIGHT,
    EXPERIENCE_WEIGHT,
    KEYWORD_WEIGHT,
    SKILL_WEIGHT,
)


def generate_screening_explanation(
    skill_score: float,
    experience_score: float,
    education_score: float,
    keyword_score: float,
    total_score: float,
) -> dict[str, str]:
    if skill_score >= SKILL_WEIGHT:
        skill_explanation = "Strong match"
    elif skill_score > 0:
        skill_explanation = "Partial match"
    else:
        skill_explanation = "No matching skills found"

    if experience_score >= EXPERIENCE_WEIGHT:
        experience_explanation = "Meets experience requirement"
    elif experience_score > 0:
        experience_explanation = "Partial experience match"
    else:
        experience_explanation = "Does not meet experience requirement"

    if education_score >= EDUCATION_WEIGHT:
        education_explanation = "Education requirement matched"
    else:
        education_explanation = "Education requirement not matched"

    if keyword_score >= KEYWORD_WEIGHT:
        keyword_explanation = "All keywords matched"
    elif keyword_score > 0:
        keyword_explanation = "Partial keyword match"
    else:
        keyword_explanation = "No matching keywords found"

    recommendation = (
        "Shortlisted"
        if total_score >= 60
        else "Rejected"
    )

    return {
        "skills": skill_explanation,
        "experience": experience_explanation,
        "education": education_explanation,
        "keywords": keyword_explanation,
        "recommendation": recommendation,
    }