import json
import time

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.resume_parser import extract_resume_text
from app.services.analysis_pipeline import run_full_analysis
from app.auth.auth_bearer import get_current_user
from app.database import get_db
from app.models.db_models import Analysis
from app.services.cache_service import (
    get_cached_result, set_cached_result, check_rate_limit
)
from app.monitoring.metrics import (
    analyses_total, pipeline_duration_seconds,
    cache_hits_total, cache_misses_total
)

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])


@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user["sub"])

    # ── Rate limiting ─────────────────────────────────────────────────────────
    allowed, remaining = check_rate_limit(user_id)
    if not allowed:
        analyses_total.labels(status="rate_limited").inc()
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Max 10 analyses per hour. Try again later."
        )

    resume_text = extract_resume_text(resume)

    # ── Redis cache check — skip pipeline if already computed ─────────────────
    cached = get_cached_result(resume_text, job_description)
    if cached:
        cache_hits_total.inc()
        analyses_total.labels(status="cache_hit").inc()
        return cached

    cache_misses_total.inc()

    # ── Run full pipeline (timed for Prometheus histogram) ────────────────────
    start = time.time()
    ctx = run_full_analysis(resume_text, job_description)
    pipeline_duration_seconds.observe(time.time() - start)

    result = {
        "ats_score":             ctx.ats_score,
        "recruiter_fit_score":   ctx.recruiter_fit_score,
        "matched_skills":        ctx.matched_skills,
        "missing_skills":        ctx.missing_skills,
        "skill_priorities":      ctx.prioritized_missing_skills,
        "section_scores":        ctx.section_scores,
        "section_feedback":      ctx.section_feedback,
        "resume_verdict":        ctx.resume_verdict,
        "interview_chance":      ctx.interview_chance,
        "fit_level":             ctx.fit_level,
        "candidate_overview":    ctx.ai_feedback.get("candidate_overview", ""),
        "strengths":             ctx.ai_feedback.get("strengths", []),
        "improvement_areas":     ctx.ai_feedback.get("improvement_areas", []),
        "recommended_actions":   ctx.ai_feedback.get("recommended_actions", []),
        "resume_audit":          ctx.resume_audit,
        "recruiter_recommendations": ctx.recommendations,
    }

    # ── Cache result for 1 hour ───────────────────────────────────────────────
    set_cached_result(resume_text, job_description, result)

    # ── Save to DB ────────────────────────────────────────────────────────────
    db.add(Analysis(
        user_id=user_id,
        job_description=job_description,
        result=json.dumps(result)
    ))
    db.commit()

    analyses_total.labels(status="success").inc()
    return result