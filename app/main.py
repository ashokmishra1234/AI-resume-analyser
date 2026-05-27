from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_resume import router

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"message": "AI Resume Analyzer Running"}
