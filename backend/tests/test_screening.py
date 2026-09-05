from app.services.screening import (
    calculate_education_score,
    calculate_experience_score,
    calculate_keyword_score,
    calculate_screening_score,
    calculate_skill_score,
    contains_term,
    extract_experience_years,
)
def test_contains_term_does_not_match_substring():
    assert contains_term(
        "I have experience with MySQL",
        "SQL",
    ) is False


def test_contains_term_matches_complete_term():
    assert contains_term(
        "I have experience with SQL",
        "SQL",
    ) is True


def test_contains_term_does_not_match_sqlalchemy():
    assert contains_term(
        "I use SQLAlchemy",
        "SQL",
    ) is False


def test_skill_matching_avoids_substring_match():
    score = calculate_skill_score(
        resume_text="Experienced with MySQL",
        required_skills="SQL",
    )

    assert score == 0.0


def test_keyword_matching_avoids_substring_match():
    score = calculate_keyword_score(
        resume_text="Experienced with SQLAlchemy",
        keywords="SQL",
    )

    assert score == 0.0

def test_normal_skill_matching():
    resume_text = """
    Python FastAPI PostgreSQL SQLAlchemy
    """

    score = calculate_skill_score(
        resume_text,
        "Python, FastAPI, PostgreSQL",
    )

    assert score == 40.0


def test_partial_skill_matching():
    resume_text = """
    Python FastAPI
    """

    score = calculate_skill_score(
        resume_text,
        "Python, FastAPI, PostgreSQL",
    )

    assert round(score, 2) == 26.67


def test_no_skill_matching():
    resume_text = """
    Java Spring Boot MySQL
    """

    score = calculate_skill_score(
        resume_text,
        "Python, FastAPI, PostgreSQL",
    )

    assert score == 0.0


def test_extract_experience_years():
    resume_text = """
    Backend Engineer with 4 years of experience
    """

    experience = extract_experience_years(
        resume_text
    )

    assert experience == 4.0


def test_extract_decimal_experience():
    resume_text = """
    Software Engineer with 2.5 years of experience
    """

    experience = extract_experience_years(
        resume_text
    )

    assert experience == 2.5


def test_experience_meets_requirement():
    resume_text = """
    Backend Engineer with 5 years of experience
    """

    score = calculate_experience_score(
        resume_text,
        3,
    )

    assert score == 25.0


def test_experience_below_requirement():
    resume_text = """
    Backend Engineer with 1 year of experience
    """

    score = calculate_experience_score(
        resume_text,
        4,
    )

    assert score == 6.25


def test_education_match():
    resume_text = """
    Bachelor of Technology in Computer Science
    """

    score = calculate_education_score(
        resume_text,
        "B.Tech",
    )

    assert score == 15.0


def test_education_exact_match():
    resume_text = """
    B.Tech in Computer Science
    """

    score = calculate_education_score(
        resume_text,
        "B.Tech",
    )

    assert score == 15.0


def test_keyword_matching():
    resume_text = """
    Python FastAPI SQLAlchemy Docker PostgreSQL
    """

    score = calculate_keyword_score(
        resume_text,
        "FastAPI, SQLAlchemy, Docker",
    )

    assert round(score, 2) == 20.0


def test_partial_keyword_matching():
    resume_text = """
    Python FastAPI Docker
    """

    score = calculate_keyword_score(
        resume_text,
        "FastAPI, SQLAlchemy, Docker",
    )

    assert round(score, 2) == 13.33


def test_complete_screening_score():
    resume_text = """
    John Doe
    B.Tech Computer Science
    Backend Engineer with 5 years of experience
    Python FastAPI PostgreSQL
    SQLAlchemy Docker
    """

    result = calculate_screening_score(
        resume_text=resume_text,
        required_skills="Python, FastAPI, PostgreSQL",
        min_experience=3,
        education="B.Tech",
        keywords="SQLAlchemy, Docker",
    )

    assert result["skill_score"] == 40.0
    assert result["experience_score"] == 25.0
    assert result["education_score"] == 15.0
    assert result["keyword_score"] == 20.0
    assert result["total_score"] == 100.0


def test_screening_score_never_exceeds_100():
    resume_text = """
    Python FastAPI PostgreSQL
    B.Tech
    10 years of experience
    SQLAlchemy Docker
    """

    result = calculate_screening_score(
        resume_text=resume_text,
        required_skills="Python, FastAPI, PostgreSQL",
        min_experience=2,
        education="B.Tech",
        keywords="SQLAlchemy, Docker",
    )

    assert result["total_score"] <= 100.0


def test_optional_requirements_do_not_reduce_score():
    resume_text = """
    Python FastAPI PostgreSQL
    """

    result = calculate_screening_score(
        resume_text=resume_text,
        required_skills="Python, FastAPI, PostgreSQL",
        min_experience=0,
        education=None,
        keywords=None,
    )

    assert result["skill_score"] == 40.0
    assert result["experience_score"] == 25.0
    assert result["education_score"] == 15.0
    assert result["keyword_score"] == 20.0
    assert result["total_score"] == 100.0