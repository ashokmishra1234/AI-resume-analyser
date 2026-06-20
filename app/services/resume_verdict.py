from app.services.ats_score import compute_interview_probability


def generate_resume_verdict(ats_score: float, recruiter_fit_score: float,
                             matched_skills: list, missing_skills: list) -> dict:
    """
    Produce three distinct scores that each answer a different question:

        ATS Score           — Will the resume pass automated keyword filters?
        Recruiter Fit Score — Would a human recruiter shortlist this person?
        Interview Chance    — Overall probability of getting an interview call?

    ATS and Recruiter Fit are computed upstream; this function combines them
    into a verdict label and interview probability.
    """
    # Verdict label is driven by ATS (the automated gate)
    if ats_score >= 80:
        verdict = "Strong Candidate"
    elif ats_score >= 60:
        verdict = "Good Candidate"
    elif ats_score >= 40:
        verdict = "Average Candidate"
    else:
        verdict = "Needs Improvement"

    # Interview chance is the combined weighted signal
    interview_chance = compute_interview_probability(ats_score, recruiter_fit_score)

    # Fit level = what % of JD-required skills the resume covers
    total = len(matched_skills) + len(missing_skills)
    fit_percentage = (len(matched_skills) / max(total, 1)) * 100
    fit_level = f"{round(fit_percentage)}%"

    return {
        "resume_verdict": verdict,
        "interview_chance": interview_chance,
        "fit_level": fit_level,
        "ats_score": ats_score,
        "recruiter_fit_score": recruiter_fit_score
    }
