from app.models.analysis_context import ResumeAnalysisContext
from app.services.resume_parser import extract_and_strip_name
from app.services.skill_matcher import match_skills
from app.services.ats_score import (
    calculate_ats_score,
    calculate_recruiter_fit_score,
    compute_interview_probability,
)
from app.services.resume_verdict import generate_resume_verdict
from app.services.section_scorer import score_sections
from app.services.skill_priority import prioritize_missing_skills
from app.services.resume_checklist import generate_resume_checklist, generate_recommendations
from app.services.ai_analyzer import generate_ai_feedback_from_facts


def _build_structured_facts(ctx: ResumeAnalysisContext) -> dict:
    """
    Flatten all computed context into a plain dict that is safe to send to the
    LLM — no raw resume text, no candidate name.
    """
    found_names = {item["name"] for item in ctx.resume_audit.get("found", [])}

    critical_missing = [
        s["skill"] for s in ctx.prioritized_missing_skills
        if s["priority"] in ("Critical", "High")
    ]
    important_missing = [
        s["skill"] for s in ctx.prioritized_missing_skills
        if s["priority"] in ("Important", "Medium")
    ]

    return {
        "ats_score": ctx.ats_score,
        "recruiter_fit_score": ctx.recruiter_fit_score,
        "resume_verdict": ctx.resume_verdict,
        "interview_chance": ctx.interview_chance,
        "fit_level": ctx.fit_level,
        "matched_skills": ctx.matched_skills,
        "critical_missing_skills": critical_missing,
        "important_missing_skills": important_missing,
        "section_scores": ctx.section_scores,
        "has_github": "GitHub Profile" in found_names,
        "has_linkedin": "LinkedIn Profile" in found_names,
        "has_metrics": "Quantified Achievements" in found_names,
        "has_experience": "Work Experience" in found_names,
        "job_title_hint": ctx.raw_job_description[:100],
    }


def run_full_analysis(resume_text: str, job_description: str) -> ResumeAnalysisContext:
    """
    Centralised analysis pipeline.  Every module reads from / writes to the
    same ResumeAnalysisContext — no module holds its own copy of raw text.

    Step order is intentional:
        Section scoring and audit run BEFORE ATS so the weighted ATS formula
        and recruiter fit score can consume their output.
    """
    ctx = ResumeAnalysisContext(
        raw_resume_text=resume_text,
        raw_job_description=job_description
    )

    # Step 1 — strip candidate name before any other module sees the text
    cleaned_text, candidate_name = extract_and_strip_name(resume_text)
    ctx.cleaned_resume_text = cleaned_text
    ctx.candidate_name = candidate_name

    # Step 2 — skill matching on cleaned text
    matched, missing = match_skills(cleaned_text, job_description)
    ctx.matched_skills = matched
    ctx.missing_skills = missing

    # Step 3 — section scoring  (must precede ATS — feeds the weighted formula)
    section_scores, section_feedback = score_sections(cleaned_text)
    ctx.section_scores = section_scores
    ctx.section_feedback = section_feedback

    # Step 4 — resume audit  (must precede recruiter fit — feeds GitHub / metrics checks)
    checklist = generate_resume_checklist(cleaned_text, job_description)
    ctx.resume_audit = checklist.get("resume_audit", {"found": [], "missing": []})

    # Step 5 — weighted ATS score (uses section scores from step 3)
    ctx.ats_score = calculate_ats_score(matched, missing, section_scores)

    # Step 6 — recruiter fit score (uses section scores + audit from steps 3 & 4)
    ctx.recruiter_fit_score = calculate_recruiter_fit_score(
        cleaned_text, matched, section_scores, ctx.resume_audit
    )

    # Step 7 — verdict + interview probability (uses both scores from steps 5 & 6)
    verdict = generate_resume_verdict(
        ctx.ats_score, ctx.recruiter_fit_score, matched, missing
    )
    ctx.resume_verdict = verdict["resume_verdict"]
    ctx.interview_chance = verdict["interview_chance"]
    ctx.fit_level = verdict["fit_level"]

    # Step 8 — prioritise missing skills by JD frequency and skill category
    ctx.prioritized_missing_skills = prioritize_missing_skills(missing, job_description)

    # Step 9 — recruiter-level actionable recommendations
    ctx.recommendations = generate_recommendations(
        ctx.resume_audit, ctx.section_scores, ctx.prioritized_missing_skills
    )

    # Step 10 — freeze all facts into a name-free dict for the LLM
    ctx.structured_facts = _build_structured_facts(ctx)

    # Step 11 — LLM feedback grounded in structured facts only
    ctx.ai_feedback = generate_ai_feedback_from_facts(ctx.structured_facts)

    return ctx
