from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import db_models
from app.api.routes_resume import router as resume_router
from app.api.routes_compare import router as compare_router
from app.api.routes_auth import router as auth_router
from app.api.routes_history import router as history_router

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(compare_router)
app.include_router(history_router)


@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"message": "AI Resume Analyzer Running"}
