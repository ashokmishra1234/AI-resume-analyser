import re

# Keywords for each section
SECTION_KEYWORDS = {
    "Education": [
        "bachelor", "master", "degree", "diploma",
        "university", "college", "school", "university",
        "gpa", "cgpa", "coursework", "certification",
        "academic", "graduation", "graduated"
    ],
    "Projects": [
        "project", "developed", "built", "created", "design",
        "implemented", "deployed", "github", "repository",
        "application", "system", "platform", "tool",
        "web", "mobile", "api", "database"
    ],
    "Skills": [
        "skilled", "proficient", "expert", "knowledge",
        "python", "java", "javascript", "typescript",
        "react", "vue", "angular", "django", "flask",
        "sql", "mongodb", "docker", "kubernetes",
        "aws", "gcp", "azure", "git", "linux"
    ],
    "Experience": [
        "experience", "worked", "worked at", "employed",
        "position", "role", "job", "responsibilities",
        "years of experience", "yr", "yrs", "year",
        "company", "organization", "enterprise",
        "intern", "junior", "senior", "manager"
    ],
    "Achievements": [
        "achievement", "award", "recognition", "achievement",
        "accomplished", "accomplished", "improved", "increased",
        "reduced", "leading", "top", "best", "successful",
        "promoted", "excellence", "honor"
    ]
}

# Feedback templates for each section based on score
FEEDBACK_TEMPLATES = {
    "Education": {
        "high": "Education section is comprehensive. Consider adding GPA and relevant coursework.",
        "medium": "Education section exists but lacks GPA and coursework details.",
        "low": "Education section is missing or unclear. Add degree, university, and graduation date."
    },
    "Projects": {
        "high": "Projects are well documented. Consider adding deployment links and GitHub URLs.",
        "medium": "Projects are mentioned but deployment links and descriptions are missing.",
        "low": "Project section is weak or missing. Add relevant project descriptions and links."
    },
    "Skills": {
        "high": "Skills section is comprehensive and well organized.",
        "medium": "Skills exist but organization could be improved. Group by category.",
        "low": "Skills section is missing or weak. Add a dedicated technical skills section."
    },
    "Experience": {
        "high": "Work experience is well documented with clear roles and achievements.",
        "medium": "Experience is present but lacks achievement metrics and impact.",
        "low": "Experience section is weak or missing. Add work history and responsibilities."
    },
    "Achievements": {
        "high": "Strong achievements with quantified results and recognition.",
        "medium": "Some achievements mentioned but more quantification would strengthen it.",
        "low": "Achievements are not clearly highlighted. Add metrics and measurable results."
    }
}


def get_feedback_level(score):
    """Categorize feedback level based on score."""
    if score >= 75:
        return "high"
    elif score >= 50:
        return "medium"
    else:
        return "low"


def score_sections(resume_text):
    """
    Analyze resume text and generate section-wise scores with feedback.
    
    Args:
        resume_text (str): The extracted resume text
    
    Returns:
        tuple: (scores dict, feedback dict)
    """
    resume_lower = resume_text.lower()
    scores = {}
    feedback = {}
    
    # Calculate score for each section
    for section, keywords in SECTION_KEYWORDS.items():
        keyword_matches = 0
        
        for keyword in keywords:
            # Count occurrences of each keyword
            matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', resume_lower))
            keyword_matches += matches
        
        # Base score calculation
        # More keywords = higher score
        if keyword_matches == 0:
            score = 0
        else:
            # Scale: 0-5 keywords = 40-60, 5-10 = 60-80, 10+ = 80-100
            if keyword_matches < 5:
                score = 40 + (keyword_matches * 4)
            elif keyword_matches < 10:
                score = 60 + (keyword_matches * 2)
            else:
                score = min(100, 80 + (keyword_matches * 1.5))
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, round(score)))
        scores[section] = score
        
        # Generate feedback
        level = get_feedback_level(score)
        feedback[section] = FEEDBACK_TEMPLATES[section][level]
    
    return scores, feedback
