import re


def calculate_ats_score(matched_skills: list, missing_skills: list, section_scores: dict = None) -> float:
    """
    Weighted ATS score that reflects how an automated screening system would
    evaluate the resume — not just skill keywords but also resume structure.

    Weights:
        Skill match    40%
        Projects       20%
        Experience     15%
        Education      10%
        Achievements   10%
        Completeness    5%
    """
    total = len(matched_skills) + len(missing_skills)
    skill_score = (len(matched_skills) / max(total, 1)) * 100

    if not section_scores:
        # No section data yet — fall back to skill-only formula
        return round(skill_score, 1)

    projects_score    = section_scores.get("Projects", 0)
    experience_score  = section_scores.get("Experience", 0)
    education_score   = section_scores.get("Education", 0)
    achievements_score = section_scores.get("Achievements", 0)

    # Completeness: how many of the 5 key sections are non-trivially present
    required_sections = ["Education", "Projects", "Skills", "Experience", "Achievements"]
    present = sum(1 for s in required_sections if section_scores.get(s, 0) > 20)
    completeness_score = (present / len(required_sections)) * 100

    weighted = (
        skill_score        * 0.40 +
        projects_score     * 0.20 +
        experience_score   * 0.15 +
        education_score    * 0.10 +
        achievements_score * 0.10 +
        completeness_score * 0.05
    )

    return round(weighted, 1)


def calculate_recruiter_fit_score(
    resume_text: str,
    matched_skills: list,
    section_scores: dict,
    audit_results: dict
) -> float:
    """
    Qualitative score modelling what a human recruiter looks for after the
    resume passes the ATS filter — action verbs, links, metrics, education, length.

    Max 100.  Weights:
        Matched skill count   25 pts
        Action verbs          20 pts
        GitHub / live links   15 pts
        Quantified metrics    20 pts
        Education present     10 pts
        Resume length          10 pts
    """
    score = 0
    resume_lower = resume_text.lower()
    found_names = {item["name"] for item in audit_results.get("found", [])}

    # 1. Matched skills signal technical alignment (3 pts each, max 25)
    score += min(len(matched_skills) * 3, 25)

    # 2. Action verbs signal professional impact
    ACTION_VERBS = [
        "built", "developed", "designed", "led", "optimized", "reduced",
        "increased", "implemented", "deployed", "managed", "created",
        "engineered", "launched", "integrated", "mentored", "architected",
    ]
    verb_hits = sum(1 for v in ACTION_VERBS if v in resume_lower)
    score += min(verb_hits * 2, 20)

    # 3. GitHub profile and live deployment links signal real-world output
    if "GitHub Profile" in found_names:
        score += 10
    if "Deployment Links" in found_names:
        score += 5

    # 4. Quantified metrics signal measurable impact ("30%", "10x", "5,000 users")
    metrics = re.findall(
        r'\d+\s*[%x]|\d[\d,]+\s*(?:users|requests|transactions|ms|records)',
        resume_lower
    )
    score += min(len(metrics) * 7, 20)

    # 5. Education section score signals academic background
    if section_scores.get("Education", 0) >= 40:
        score += 10

    # 6. Resume length: too short = thin, too long = unfocused
    word_count = len(resume_lower.split())
    if 300 <= word_count <= 800:
        score += 10
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        score += 5

    return round(min(score, 100), 1)


def compute_interview_probability(ats_score: float, recruiter_fit_score: float) -> str:
    """
    Combined score: ATS gates the initial shortlist (40%), recruiter makes
    the actual call (60%).  Returns a human-readable probability label.
    """
    combined = (ats_score * 0.4) + (recruiter_fit_score * 0.6)

    if combined >= 75:
        return "Very High"
    if combined >= 60:
        return "High"
    if combined >= 45:
        return "Medium"
    return "Low"
