def generate_resume_verdict(ats_score, matched_skills, missing_skills):
    """
    Generate resume verdict and interview chance based on ATS score.
    
    Args:
        ats_score (int): ATS score 0-100
        matched_skills (list): Matched skills
        missing_skills (list): Missing skills
    
    Returns:
        dict: Verdict, interview chance, and fit level
    """
    
    if ats_score >= 80:
        verdict = "Strong Candidate"
        interview_chance = "High"
    elif ats_score >= 60:
        verdict = "Good Candidate"
        interview_chance = "Medium"
    elif ats_score >= 40:
        verdict = "Average Candidate"
        interview_chance = "Low"
    else:
        verdict = "Needs Improvement"
        interview_chance = "Very Low"
    
    # Calculate fit level
    total_skills = len(matched_skills) + len(missing_skills)
    if total_skills == 0:
        fit_level = "0%"
    else:
        fit_percentage = (len(matched_skills) / total_skills) * 100
        fit_level = f"{round(fit_percentage)}%"
    
    return {
        "resume_verdict": verdict,
        "interview_chance": interview_chance,
        "fit_level": fit_level,
        "ats_score": ats_score
    }
