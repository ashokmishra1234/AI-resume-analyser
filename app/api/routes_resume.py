from fastapi import APIRouter, UploadFile, File, Form

from app.services.resume_parser import extract_resume_text
from app.services.skill_matcher import match_skills
from app.services.ats_score import calculate_ats_score
from app.services.ai_analyzer import generate_ai_feedback

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_resume_text(resume)

    matched_skills, missing_skills = match_skills(
        resume_text,
        job_description
    )

    ats_score = calculate_ats_score(
        matched_skills,
        missing_skills
    )

    ai_feedback = generate_ai_feedback(
        resume_text,
        job_description
    )

    return {
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "summary": ai_feedback["summary"],
        "suggestions": ai_feedback["suggestions"]
    }
