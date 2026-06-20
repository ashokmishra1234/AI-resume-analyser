import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Analysis
from app.auth.auth_bearer import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/")
def get_history(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(current_user["sub"])

    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    result = []
    for analysis in analyses:
        data = json.loads(analysis.result)
        result.append({
            "id": analysis.id,
            "created_at": analysis.created_at.isoformat(),
            "job_description_preview": analysis.job_description[:100] + "..." if len(analysis.job_description) > 100 else analysis.job_description,
            "ats_score": data.get("ats_score"),
            "resume_verdict": data.get("resume_verdict"),
            "fit_level": data.get("fit_level"),
            "interview_chance": data.get("interview_chance"),
        })

    return result
