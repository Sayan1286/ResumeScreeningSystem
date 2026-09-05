import re


SKILL_WEIGHT = 40
EXPERIENCE_WEIGHT = 25
EDUCATION_WEIGHT = 15
KEYWORD_WEIGHT = 20


EDUCATION_ALIASES = {
    "b.tech": [
        "b.tech",
        "btech",
        "bachelor of technology",
    ],
    "b.e": [
        "b.e",
        "be",
        "bachelor of engineering",
    ],
    "b.sc": [
        "b.sc",
        "bsc",
        "bachelor of science",
    ],
    "m.tech": [
        "m.tech",
        "mtech",
        "master of technology",
    ],
    "m.e": [
        "m.e",
        "me",
        "master of engineering",
    ],
    "m.sc": [
        "m.sc",
        "msc",
        "master of science",
    ],
    "mba": [
        "mba",
        "master of business administration",
    ],
    "phd": [
        "phd",
        "ph.d",
        "doctor of philosophy",
    ],
}


def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower().strip(),
    )


def parse_list(value: str | None) -> list[str]:
    if not value:
        return []

    return [
        item.strip().lower()
        for item in value.split(",")
        if item.strip()
    ]


def contains_term(text: str, term: str) -> bool:
    escaped_term = re.escape(term.strip().lower())

    pattern = rf"(?<!\w){escaped_term}(?!\w)"

    return re.search(
        pattern,
        text,
        re.IGNORECASE,
    ) is not None


def calculate_skill_score(
    resume_text: str,
    required_skills: str,
) -> float:
    resume = normalize_text(resume_text)
    skills = parse_list(required_skills)

    if not skills:
        return 0.0

    matched = sum(
        1
        for skill in skills
        if contains_term(resume, skill)
    )

    return (matched / len(skills)) * SKILL_WEIGHT


def extract_experience_years(resume_text: str) -> float:
    text = normalize_text(resume_text)

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:professional\s+)?experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+experience",
    ]

    matches = []

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            matches.append(float(match.group(1)))

    if not matches:
        return 0.0

    return max(matches)


def calculate_experience_score(
    resume_text: str,
    min_experience: int,
) -> float:
    if min_experience <= 0:
        return EXPERIENCE_WEIGHT

    experience_years = extract_experience_years(
        resume_text
    )

    if experience_years >= min_experience:
        return EXPERIENCE_WEIGHT

    return (
        experience_years / min_experience
    ) * EXPERIENCE_WEIGHT


def calculate_education_score(
    resume_text: str,
    education: str | None,
) -> float:
    if not education:
        return EDUCATION_WEIGHT

    resume = normalize_text(resume_text)
    required_education = normalize_text(education)

    aliases = EDUCATION_ALIASES.get(
        required_education,
        [required_education],
    )

    if any(
        contains_term(resume, alias)
        for alias in aliases
    ):
        return EDUCATION_WEIGHT

    return 0.0


def calculate_keyword_score(
    resume_text: str,
    keywords: str | None,
) -> float:
    keyword_list = parse_list(keywords)

    if not keyword_list:
        return KEYWORD_WEIGHT

    resume = normalize_text(resume_text)

    matched = sum(
        1
        for keyword in keyword_list
        if contains_term(resume, keyword)
    )

    return (
        matched / len(keyword_list)
    ) * KEYWORD_WEIGHT


def calculate_screening_score(
    resume_text: str,
    required_skills: str,
    min_experience: int,
    education: str | None,
    keywords: str | None,
) -> dict[str, float]:
    skill_score = calculate_skill_score(
        resume_text,
        required_skills,
    )

    experience_score = calculate_experience_score(
        resume_text,
        min_experience,
    )

    education_score = calculate_education_score(
        resume_text,
        education,
    )

    keyword_score = calculate_keyword_score(
        resume_text,
        keywords,
    )

    total_score = (
        skill_score
        + experience_score
        + education_score
        + keyword_score
    )

    return {
        "skill_score": round(skill_score, 2),
        "experience_score": round(
            experience_score,
            2,
        ),
        "education_score": round(
            education_score,
            2,
        ),
        "keyword_score": round(
            keyword_score,
            2,
        ),
        "total_score": round(
            total_score,
            2,
        ),
    }