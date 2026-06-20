from fastapi import APIRouter, UploadFile, File, Form, Depends

from app.services.resume_parser import extract_resume_text
from app.services.skill_matcher import match_skills
from app.services.ats_score import calculate_ats_score
from app.services.resume_comparator import compare_resumes
from app.services.section_scorer import score_sections
from app.auth.auth_bearer import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume Comparison"])


@router.post("/compare")
async def compare_two_resumes(
    resume1: UploadFile = File(...),
    resume2: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    resume1_text = extract_resume_text(resume1)
    resume2_text = extract_resume_text(resume2)

    matched1, missing1 = match_skills(resume1_text, job_description)
    # score_sections returns (scores_dict, feedback_dict) — unpack properly
    section_scores_1, _ = score_sections(resume1_text)
    ats_score_1 = calculate_ats_score(matched1, missing1, section_scores_1)

    matched2, missing2 = match_skills(resume2_text, job_description)
    section_scores_2, _ = score_sections(resume2_text)
    ats_score_2 = calculate_ats_score(matched2, missing2, section_scores_2)

    comparison = compare_resumes(ats_score_1, ats_score_2)

    return {
        "resume1": {
            "ats_score": ats_score_1,
            "matched_skills": matched1,
            "missing_skills": missing1,
            "section_scores": section_scores_1
        },
        "resume2": {
            "ats_score": ats_score_2,
            "matched_skills": matched2,
            "missing_skills": missing2,
            "section_scores": section_scores_2
        },
        "comparison": {
            "winner": comparison["winner"],
            "resume1_score": comparison["resume1_score"],
            "resume2_score": comparison["resume2_score"],
            "difference": comparison["difference"]
        }
    }
