import re


def generate_resume_checklist(resume_text, job_description):
    """
    Audit resume content and return found vs missing items.
    
    Args:
        resume_text (str): Extracted resume text
        job_description (str): Job description
    
    Returns:
        dict: Resume audit with found and missing items
    """
    
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    found = []
    missing = []
    
    # Define all checklist items with their priorities
    checklist_items = [
        {
            "name": "GitHub Profile",
            "priority": "High",
            "keywords": ["github", "github.com"]
        },
        {
            "name": "LinkedIn Profile",
            "priority": "High",
            "keywords": ["linkedin", "linkedin.com"]
        },
        {
            "name": "Portfolio Website",
            "priority": "Medium",
            "keywords": ["portfolio", "website", "personal website"]
        },
        {
            "name": "Deployment Links",
            "priority": "High",
            "keywords": ["deploy", "heroku", "vercel", "netlify", "aws", "azure", "gcp", "deployed"]
        },
        {
            "name": "Quantified Achievements",
            "priority": "High",
            "keywords": [r'\d+%', r'\d+x', "increased", "improved", "reduced", "achieved"]
        },
        {
            "name": "Certifications",
            "priority": "Medium",
            "keywords": ["certification", "certified", "certificate"]
        },
        {
            "name": "Work Experience",
            "priority": "High",
            "keywords": ["experience", "worked", "intern", "position", "employment"]
        },
        {
            "name": "Education Section",
            "priority": "High",
            "keywords": ["bachelor", "master", "degree", "university", "college"]
        },
        {
            "name": "Skills Section",
            "priority": "High",
            "keywords": ["skill", "skills", "technical skill"]
        },
        {
            "name": "Action Verbs",
            "priority": "Medium",
            "keywords": ["developed", "designed", "implemented", "created", "built", "managed", "led", "achieved", "improved", "optimized"]
        },
        {
            "name": "Relevant Technologies",
            "priority": "High",
            "keywords": ["python", "java", "javascript", "react", "docker", "aws", "kubernetes", "sql", "mongodb"]
        }
    ]
    
    # Check each item
    for item in checklist_items:
        is_present = False
        
        # Check if any keyword is present
        for keyword in item["keywords"]:
            if keyword.startswith(r'\d'):
                # Regex pattern
                if re.search(keyword, resume_lower):
                    is_present = True
                    break
            else:
                # Simple string match
                if keyword in resume_lower:
                    is_present = True
                    break
        
        if is_present:
            found.append({
                "name": item["name"],
                "priority": item["priority"]
            })
        else:
            missing.append({
                "name": item["name"],
                "priority": item["priority"]
            })
    
    return {
        "resume_audit": {
            "found": found,
            "missing": missing
        }
    }


def generate_recommendations(resume_audit: dict, section_scores: dict,
                              prioritized_missing_skills: list) -> list:
    """
    Generate up to 5 specific, actionable recommendations based on audit
    results, section quality, and missing skills.  More concrete than generic
    'learn X' suggestions.
    """
    recs = []
    found_names = {item["name"] for item in resume_audit.get("found", [])}
    missing_names = {item["name"] for item in resume_audit.get("missing", [])}

    if "GitHub Profile" in missing_names:
        recs.append("Add a GitHub profile link — recruiters expect to see your code.")

    if "Deployment Links" in missing_names:
        recs.append("Deploy at least one project and add the live URL to your resume.")

    if "Quantified Achievements" in missing_names:
        recs.append("Add 2–3 metrics to your projects or experience (e.g. 'reduced load time by 30%', 'served 5,000 users').")

    if section_scores.get("Experience", 100) < 40:
        recs.append("Rewrite experience bullet points starting with action verbs: Built, Developed, Optimised, Reduced.")

    if section_scores.get("Projects", 100) < 40:
        recs.append("Add at least 2 end-to-end projects with tech stack, description, and a GitHub or live link.")

    if "LinkedIn Profile" in missing_names:
        recs.append("Add your LinkedIn profile URL — many ATS systems cross-reference it.")

    critical = [s["skill"] for s in prioritized_missing_skills if s["priority"] in ("High", "Critical")]
    if critical:
        recs.append(f"Build one project using {critical[0]} to close the most critical skill gap for this role.")

    if section_scores.get("Achievements", 100) < 40:
        recs.append("Add certifications, hackathon results, or academic rankings to the Achievements section.")

    return recs[:5]
