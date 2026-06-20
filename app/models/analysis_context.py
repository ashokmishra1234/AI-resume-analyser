from dataclasses import dataclass, field


@dataclass
class ResumeAnalysisContext:
    """Single shared object that flows through every analysis step."""

    raw_resume_text: str
    raw_job_description: str

    # After name stripping (Problem 2)
    cleaned_resume_text: str = ""
    candidate_name: str = ""

    # After skill matching (Problem 5)
    matched_skills: list = field(default_factory=list)
    missing_skills: list = field(default_factory=list)

    # After scoring
    ats_score: float = 0.0
    recruiter_fit_score: float = 0.0
    resume_verdict: str = ""
    interview_chance: str = ""
    fit_level: str = ""

    # After section scoring
    section_scores: dict = field(default_factory=dict)
    section_feedback: dict = field(default_factory=dict)

    # After skill prioritization
    prioritized_missing_skills: list = field(default_factory=list)

    # After resume audit
    resume_audit: dict = field(default_factory=dict)
    recommendations: list = field(default_factory=list)

    # Structured facts built from all above — what LLM receives (Problem 10)
    structured_facts: dict = field(default_factory=dict)

    # Final AI feedback
    ai_feedback: dict = field(default_factory=dict)
