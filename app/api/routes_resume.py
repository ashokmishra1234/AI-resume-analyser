from fastapi import APIRouter, UploadFile, File, Form

from app.services.resume_parser import extract_resume_text
from app.services.skill_matcher import match_skills
from app.services.ats_score import calculate_ats_score
from app.services.ai_analyzer import generate_ai_feedback
from app.services.section_scorer import score_sections
from app.services.resume_verdict import generate_resume_verdict
from app.services.skill_priority import prioritize_missing_skills
from app.services.resume_checklist import generate_resume_checklist

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Comprehensive resume analysis endpoint.
    
    Returns:
    - ATS score
    - Matched and missing skills with priorities
    - Section scores with feedback
    - Resume verdict and interview chance
    - AI-powered analysis
    - Resume improvement checklist
    """
    
    # Extract resume text
    resume_text = extract_resume_text(resume)

    # Calculate skill match
    matched_skills, missing_skills = match_skills(
        resume_text,
        job_description
    )

    # Calculate ATS score
    ats_score = calculate_ats_score(
        matched_skills,
        missing_skills
    )

    # Generate resume verdict
    verdict = generate_resume_verdict(
        ats_score,
        matched_skills,
        missing_skills
    )

    # Get section scores and feedback
    section_scores, section_feedback = score_sections(resume_text)

    # Prioritize missing skills
    prioritized_missing_skills = prioritize_missing_skills(
        missing_skills,
        job_description
    )

    # Generate AI feedback
    ai_feedback = generate_ai_feedback(
        resume_text,
        job_description
    )

    # Generate resume checklist
    checklist_data = generate_resume_checklist(resume_text, job_description)

    return {
        # Core scores
        "ats_score": ats_score,
        
        # Skills analysis
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_priorities": prioritized_missing_skills,
        
        # Section analysis
        "section_scores": section_scores,
        "section_feedback": section_feedback,
        
        # Verdict
        "resume_verdict": verdict["resume_verdict"],
        "interview_chance": verdict["interview_chance"],
        "fit_level": verdict["fit_level"],
        
        # AI analysis
        "candidate_overview": ai_feedback.get("candidate_overview", ""),
        "strengths": ai_feedback.get("strengths", []),
        "improvement_areas": ai_feedback.get("improvement_areas", []),
        "recommended_actions": ai_feedback.get("recommended_actions", []),
        
        # Resume audit
        "resume_audit": checklist_data.get("resume_audit", {"found": [], "missing": []})
    }

