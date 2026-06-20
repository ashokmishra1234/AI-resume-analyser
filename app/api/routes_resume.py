import json

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.services.resume_parser import extract_resume_text
from app.services.analysis_pipeline import run_full_analysis
from app.auth.auth_bearer import get_current_user
from app.database import get_db
from app.models.db_models import Analysis

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Extract raw text from PDF upload
    resume_text = extract_resume_text(resume)

    # Run the full centralised pipeline
    ctx = run_full_analysis(resume_text, job_description)

    result = {
        "ats_score": ctx.ats_score,
        "recruiter_fit_score": ctx.recruiter_fit_score,
        "matched_skills": ctx.matched_skills,
        "missing_skills": ctx.missing_skills,
        "skill_priorities": ctx.prioritized_missing_skills,
        "section_scores": ctx.section_scores,
        "section_feedback": ctx.section_feedback,
        "resume_verdict": ctx.resume_verdict,
        "interview_chance": ctx.interview_chance,
        "fit_level": ctx.fit_level,
        "candidate_overview": ctx.ai_feedback.get("candidate_overview", ""),
        "strengths": ctx.ai_feedback.get("strengths", []),
        "improvement_areas": ctx.ai_feedback.get("improvement_areas", []),
        "recommended_actions": ctx.ai_feedback.get("recommended_actions", []),
        "resume_audit": ctx.resume_audit,
        "recruiter_recommendations": ctx.recommendations
    }

    db.add(Analysis(
        user_id=int(current_user["sub"]),
        job_description=job_description,
        result=json.dumps(result)
    ))
    db.commit()

    return result
