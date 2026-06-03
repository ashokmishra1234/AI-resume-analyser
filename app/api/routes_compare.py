from fastapi import APIRouter, UploadFile, File, Form

from app.services.resume_parser import extract_resume_text
from app.services.skill_matcher import match_skills
from app.services.ats_score import calculate_ats_score
from app.services.resume_comparator import compare_resumes
from app.services.section_scorer import score_sections

router = APIRouter(prefix="/resume", tags=["Resume Comparison"])


@router.post("/compare")
async def compare_two_resumes(
    resume1: UploadFile = File(...),
    resume2: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Compare two resumes against a job description.
    
    Args:
        resume1: First resume PDF file
        resume2: Second resume PDF file
        job_description: Job description text
    
    Returns:
        Comparison results with ATS scores and winner
    """
    
    # Extract text from both resumes
    resume1_text = extract_resume_text(resume1)
    resume2_text = extract_resume_text(resume2)
    
    # Calculate scores for resume 1
    matched_skills_1, missing_skills_1 = match_skills(
        resume1_text,
        job_description
    )
    ats_score_1 = calculate_ats_score(
        matched_skills_1,
        missing_skills_1
    )
    section_scores_1 = score_sections(resume1_text)
    
    # Calculate scores for resume 2
    matched_skills_2, missing_skills_2 = match_skills(
        resume2_text,
        job_description
    )
    ats_score_2 = calculate_ats_score(
        matched_skills_2,
        missing_skills_2
    )
    section_scores_2 = score_sections(resume2_text)
    
    # Compare resumes
    comparison = compare_resumes(ats_score_1, ats_score_2)
    
    return {
        "resume1": {
            "ats_score": ats_score_1,
            "matched_skills": matched_skills_1,
            "missing_skills": missing_skills_1,
            "section_scores": section_scores_1
        },
        "resume2": {
            "ats_score": ats_score_2,
            "matched_skills": matched_skills_2,
            "missing_skills": missing_skills_2,
            "section_scores": section_scores_2
        },
        "comparison": {
            "winner": comparison["winner"],
            "resume1_score": comparison["resume1_score"],
            "resume2_score": comparison["resume2_score"],
            "difference": comparison["difference"]
        }
    }
