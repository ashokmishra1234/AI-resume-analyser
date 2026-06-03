# Core skills from job description = High priority
CORE_SKILL_KEYWORDS = [
    "python", "java", "javascript", "react", "node.js",
    "fastapi", "django", "express", "database", "sql",
    "api", "rest", "graphql", "microservices", "docker"
]

# Preferred skills = Medium priority
PREFERRED_SKILL_KEYWORDS = [
    "aws", "gcp", "azure", "kubernetes", "ci/cd",
    "git", "testing", "agile", "scrum", "jira",
    "mongodb", "redis", "elasticsearch"
]

# Optional skills = Low priority
OPTIONAL_SKILL_KEYWORDS = [
    "machine learning", "ai", "blockchain", "ml",
    "data science", "analytics", "devops",
    "security", "compliance", "optimization"
]


def prioritize_missing_skills(missing_skills, job_description):
    """
    Prioritize missing skills based on job description context.
    
    Args:
        missing_skills (list): Skills that are missing from resume
        job_description (str): Job description text
    
    Returns:
        list: Missing skills with priority levels
    """
    
    job_desc_lower = job_description.lower()
    prioritized = []
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        priority = "Low"
        
        # Check if skill appears in core keywords
        for core_skill in CORE_SKILL_KEYWORDS:
            if core_skill in skill_lower or skill_lower in job_desc_lower:
                priority = "High"
                break
        
        # Check if skill appears in preferred keywords
        if priority == "Low":
            for pref_skill in PREFERRED_SKILL_KEYWORDS:
                if pref_skill in skill_lower:
                    priority = "Medium"
                    break
        
        # Check how many times skill appears in job description
        if skill_lower in job_description.lower():
            if priority == "Low":
                priority = "Medium"
            elif priority == "Medium":
                priority = "High"
        
        prioritized.append({
            "skill": skill,
            "priority": priority
        })
    
    # Sort by priority: High > Medium > Low
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    prioritized.sort(key=lambda x: priority_order[x["priority"]])
    
    return prioritized
