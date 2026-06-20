import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.services.skill_matcher import match_skills

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# Injected into every LLM call — enforces name-free, evidence-only output
SYSTEM_PROMPT = """You are a professional resume analyst.

CRITICAL RULES — follow these exactly:
1. NEVER use any person's name. Always say "the candidate" or "the applicant".
2. Only generate feedback that is directly supported by the structured data you receive.
3. Never invent strengths. Only mention a strength if it appears in matched_skills or a section score >= 70.
4. Never invent weaknesses. Only mention a gap if it appears in critical_missing_skills or a section score < 40.
5. Reference specific scores, skill names, or audit flags to justify every statement.
6. Write in third person only. Never use "you" or "your"."""


def parse_structured_response(content: str) -> dict | None:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except Exception:
            pass
    return None


def generate_fallback_from_facts(facts: dict) -> dict:
    """Rule-based feedback used when the LLM API is unavailable."""
    ats = facts.get("ats_score", 0)
    matched = facts.get("matched_skills", [])
    critical_missing = facts.get("critical_missing_skills", [])
    verdict = facts.get("resume_verdict", "Needs Improvement")
    section_scores = facts.get("section_scores", {})

    overview = f"The candidate received an ATS score of {ats}% with a verdict of '{verdict}'."
    if matched:
        overview += f" Key matched skills include {', '.join(matched[:3])}."

    strengths = []
    if matched:
        strengths.append(f"The candidate demonstrates proficiency in {', '.join(matched[:3])}")
    for section, score in section_scores.items():
        if score >= 70 and len(strengths) < 3:
            strengths.append(f"{section} section is strong (score: {score}%)")
    if not strengths:
        strengths = ["The candidate has relevant technical knowledge in the resume"]

    improvements = [
        f"The candidate is missing '{s}', which is a critical requirement for this role"
        for s in critical_missing[:3]
    ]
    if not improvements:
        improvements = ["Expanding the technical skill set would improve alignment with the job requirements"]

    actions = []
    if not facts.get("has_github"):
        actions.append("Add a GitHub profile link to the resume")
    if not facts.get("has_metrics"):
        actions.append("Add quantified achievements such as 'reduced load time by 30%' or 'served 5,000 users'")
    if critical_missing:
        actions.append(
            f"Build a project demonstrating {critical_missing[0]} to address the most critical skill gap"
        )
    if not actions:
        actions = ["Continue building technically relevant projects to strengthen the overall profile"]

    return {
        "candidate_overview": overview,
        "strengths": strengths[:3],
        "improvement_areas": improvements[:3],
        "recommended_actions": actions[:3]
    }


def generate_ai_feedback_from_facts(structured_facts: dict) -> dict:
    """
    Primary feedback function. Receives pre-computed structured facts (no raw resume text,
    no candidate name) and generates grounded, evidence-based feedback via the LLM.
    Falls back to rule-based output if the LLM call fails.
    """
    try:
        facts_json = json.dumps(structured_facts, indent=2)

        prompt = f"""Generate resume feedback based ONLY on the structured analysis data below.
Do not reference any information not present in this data.

ANALYSIS DATA:
{facts_json}

Respond in this EXACT JSON format — no markdown, no extra text outside the JSON:
{{
  "candidate_overview": "2-3 sentences referencing ats_score, resume_verdict, and matched_skills",
  "strengths": [
    "Strength tied to a specific matched skill or high section score",
    "Strength 2 with data reference",
    "Strength 3 with data reference"
  ],
  "improvement_areas": [
    "Gap tied to a specific critical_missing_skill or low section score",
    "Improvement area 2",
    "Improvement area 3"
  ],
  "recommended_actions": [
    "Specific concrete action referencing a missing skill, audit flag, or low score",
    "Action 2",
    "Action 3"
  ]
}}"""

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])

        parsed = parse_structured_response(response.content)

        if parsed and isinstance(parsed, dict):
            required = ["candidate_overview", "strengths", "improvement_areas", "recommended_actions"]
            if all(k in parsed for k in required):
                return {
                    "candidate_overview": parsed["candidate_overview"],
                    "strengths": parsed["strengths"],
                    "improvement_areas": parsed["improvement_areas"],
                    "recommended_actions": parsed["recommended_actions"]
                }

        return _parse_text_response(response.content)

    except Exception as e:
        print(f"LLM API failed: {e}. Using structured fallback.")
        return generate_fallback_from_facts(structured_facts)


def _parse_text_response(content: str) -> dict:
    """Last-resort parser when the LLM returns plain text instead of JSON."""
    lines = content.split('\n')
    overview = ""
    strengths = []
    improvements = []
    actions = []
    current_section = None

    for line in lines:
        line = line.strip()
        if "overview" in line.lower():
            current_section = "overview"
        elif "strength" in line.lower():
            current_section = "strengths"
        elif "improvement" in line.lower():
            current_section = "improvements"
        elif "action" in line.lower() or "recommendation" in line.lower():
            current_section = "actions"
        elif line and not line.startswith("**"):
            if current_section == "overview":
                overview = line
            elif current_section == "strengths" and (line.startswith("-") or line.startswith("•")):
                strengths.append(line.lstrip("-• "))
            elif current_section == "improvements" and (line.startswith("-") or line.startswith("•")):
                improvements.append(line.lstrip("-• "))
            elif current_section == "actions" and (line.startswith("-") or line.startswith("•")):
                actions.append(line.lstrip("-• "))

    return {
        "candidate_overview": overview or "The candidate has a relevant technical background for this role.",
        "strengths": strengths or ["Technical skills are present in the resume"],
        "improvement_areas": improvements or ["Expanding the technical skill set would improve role alignment"],
        "recommended_actions": actions or ["Build more relevant projects to strengthen the profile"]
    }


def generate_ai_feedback(resume_text: str, job_description: str) -> dict:
    """
    Legacy entry point kept for backward compatibility.
    Builds a minimal facts dict from raw text and delegates to generate_ai_feedback_from_facts.
    """
    matched_skills, missing_skills = match_skills(resume_text, job_description)
    total = len(matched_skills) + len(missing_skills)

    minimal_facts = {
        "ats_score": round(len(matched_skills) / max(total, 1) * 100),
        "resume_verdict": "Analysis",
        "interview_chance": "Unknown",
        "fit_level": "Unknown",
        "matched_skills": matched_skills,
        "critical_missing_skills": missing_skills[:5],
        "important_missing_skills": [],
        "section_scores": {},
        "has_github": "github" in resume_text.lower(),
        "has_linkedin": "linkedin" in resume_text.lower(),
        "has_metrics": False,
        "has_experience": "experience" in resume_text.lower(),
        "job_title_hint": job_description[:100]
    }

    return generate_ai_feedback_from_facts(minimal_facts)
