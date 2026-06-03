import os
import json

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.services.nlp_fallback import basic_resume_analysis
from app.services.skill_matcher import match_skills

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


def parse_structured_response(content):
    """
    Try to parse structured JSON from LLM response.
    Falls back to extracting structured data if JSON parsing fails.
    
    Args:
        content (str): LLM response content
    
    Returns:
        dict: Structured analysis
    """
    
    try:
        # Try to parse JSON directly
        return json.loads(content)
    except json.JSONDecodeError:
        # If direct parsing fails, try to extract JSON from content
        try:
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass
    
    # Fallback: parse the response manually
    return None


def generate_ai_feedback(resume_text, job_description):
    """
    Generate structured AI feedback for resume analysis.
    Falls back to rule-based analysis if LLM API fails.
    
    Args:
        resume_text (str): Extracted resume text
        job_description (str): Job description provided by user
    
    Returns:
        dict: Structured analysis with candidate overview, strengths, improvements, and actions
    """
    
    try:
        prompt = f"""
Analyze this resume against the given job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide a response in the following EXACT JSON format (no markdown, no extra text):

{{
  "candidate_overview": "Brief 2-3 sentence summary of the candidate's profile and fit",
  "strengths": [
    "Strength 1",
    "Strength 2",
    "Strength 3"
  ],
  "improvement_areas": [
    "Area for improvement 1",
    "Area for improvement 2",
    "Area for improvement 3"
  ],
  "recommended_actions": [
    "Action 1 to take",
    "Action 2 to take",
    "Action 3 to take"
  ]
}}

Keep each item concise and professional. Do not include any text outside the JSON object.
"""

        response = llm.invoke([
            HumanMessage(content=prompt)
        ])

        content = response.content
        
        # Try to parse structured response
        parsed = parse_structured_response(content)
        
        if parsed and isinstance(parsed, dict):
            # Validate structure
            required_keys = ["candidate_overview", "strengths", "improvement_areas", "recommended_actions"]
            if all(key in parsed for key in required_keys):
                return {
                    "candidate_overview": parsed.get("candidate_overview", ""),
                    "strengths": parsed.get("strengths", []),
                    "improvement_areas": parsed.get("improvement_areas", []),
                    "recommended_actions": parsed.get("recommended_actions", [])
                }
        
        # If parsing failed, parse manually from text response
        return parse_text_response(content)
    
    except Exception as e:
        # Fallback to rule-based analysis if LLM fails
        print(f"LLM API failed: {str(e)}. Using fallback analysis.")
        
        matched_skills, missing_skills = match_skills(resume_text, job_description)
        
        fallback_result = basic_resume_analysis(matched_skills, missing_skills)
        
        return fallback_result


def parse_text_response(content):
    """
    Parse structured data from plain text response.
    
    Args:
        content (str): LLM response content
    
    Returns:
        dict: Structured analysis
    """
    
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
            elif current_section == "strengths" and line.startswith("-"):
                strengths.append(line.lstrip("- ").lstrip("• "))
            elif current_section == "improvements" and line.startswith("-"):
                improvements.append(line.lstrip("- ").lstrip("• "))
            elif current_section == "actions" and line.startswith("-"):
                actions.append(line.lstrip("- ").lstrip("• "))
    
    return {
        "candidate_overview": overview or "Professional candidate with relevant experience.",
        "strengths": strengths if strengths else ["Strong technical background", "Good fit for role"],
        "improvement_areas": improvements if improvements else ["Gain more experience", "Expand skill set"],
        "recommended_actions": actions if actions else ["Build more projects", "Learn new technologies"]
    }
