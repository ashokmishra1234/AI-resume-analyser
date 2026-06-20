import re

FEEDBACK_TEMPLATES = {
    "Education": {
        "high":   "Education section is strong — degree, institution, and details are present.",
        "medium": "Education section exists but is missing GPA, graduation year, or field of study.",
        "low":    "Education section is weak or missing — add degree, university, and graduation date."
    },
    "Projects": {
        "high":   "Projects are well documented with tech stack and links.",
        "medium": "Projects are mentioned but lack deployment links, GitHub URLs, or impact metrics.",
        "low":    "Project section is weak — add descriptions, tech stack, and at least one link."
    },
    "Skills": {
        "high":   "Skills section is comprehensive and covers a good range of technologies.",
        "medium": "Skills section exists but could be more specific — group by category.",
        "low":    "Skills section is missing or very thin — add a dedicated technical skills list."
    },
    "Experience": {
        "high":   "Work experience is well documented with roles, impact, and action verbs.",
        "medium": "Experience is present but lacks quantified achievements or action verbs.",
        "low":    "Experience section is weak or missing — add work history and responsibilities."
    },
    "Achievements": {
        "high":   "Achievements are highlighted with measurable results and recognition.",
        "medium": "Some achievements are mentioned but more metrics or certifications would help.",
        "low":    "Achievements section is missing — add certifications, rankings, or awards."
    }
}

TECH_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "vue", "angular",
    "fastapi", "django", "flask", "node", "express", "spring",
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "sql",
    "docker", "kubernetes", "aws", "gcp", "azure", "git", "linux",
    "tensorflow", "pytorch", "machine learning", "html", "css", "tailwind",
]

ACTION_VERBS = [
    "built", "developed", "designed", "led", "managed", "optimized",
    "reduced", "increased", "implemented", "deployed", "created",
    "engineered", "launched", "integrated", "architected", "mentored",
]

DEGREE_KEYWORDS = ["bachelor", "master", "b.tech", "b.e", "bsc", "msc", "m.tech", "phd", "degree", "diploma"]
COLLEGE_KEYWORDS = ["university", "college", "institute", "iit", "nit", "bits", "vit", "srm", "manipal"]
CERT_KEYWORDS    = ["certified", "certification", "certificate", "coursera", "udemy", "hackerrank", "leetcode"]
RANK_KEYWORDS    = ["rank", "winner", "1st", "2nd", "finalist", "hackathon", "olympiad", "award", "scholarship"]


def _feedback_level(score: int) -> str:
    if score >= 70: return "high"
    if score >= 40: return "medium"
    return "low"


def _score_education(text: str) -> int:
    t = text.lower()
    score = 0
    if any(k in t for k in DEGREE_KEYWORDS):                             score += 30
    if any(k in t for k in COLLEGE_KEYWORDS):                            score += 20
    if re.search(r'(cgpa|gpa|percentage)\s*[:\-]?\s*[\d.]+', t):        score += 25
    if re.search(r'\b20[0-2]\d\b', t):                                   score += 15  # graduation year
    if re.search(r'(computer science|information technology|software|data)', t): score += 10
    return min(score, 100)


def _score_projects(text: str) -> int:
    t = text.lower()
    score = 0
    tech_hits = sum(1 for s in TECH_SKILLS if s in t)
    score += min(tech_hits * 5, 30)                                       # tech stack variety
    if re.search(r'github\.com/\S+', t):                                  score += 20  # GitHub link
    if re.search(r'(vercel|netlify|heroku|\.live|\.app|deployed)', t):   score += 20  # live link
    if re.search(r'\d+\s*[%x]|\d[\d,]+\s*(users|requests)', t):         score += 20  # metrics
    # rough project count: capitalised lines or bullet starts
    project_count = len(re.findall(r'\n[A-Z][^\n]{5,60}\n', text))
    score += min(project_count * 5, 10)
    return min(score, 100)


def _score_skills(text: str) -> int:
    t = text.lower()
    tech_hits = sum(1 for s in TECH_SKILLS if s in t)
    return min(tech_hits * 7, 100)


def _score_experience(text: str) -> int:
    t = text.lower()
    score = 0
    if re.search(r'(experience|intern|worked|employed|position|role)', t): score += 20
    verb_hits = sum(1 for v in ACTION_VERBS if v in t)
    score += min(verb_hits * 5, 35)
    if re.search(r'\d+\s*[%x]|\d[\d,]+\s*(users|requests|records)', t): score += 25
    tech_hits = sum(1 for s in TECH_SKILLS if s in t)
    score += min(tech_hits * 4, 20)
    return min(score, 100)


def _score_achievements(text: str) -> int:
    t = text.lower()
    score = 0
    if any(k in t for k in CERT_KEYWORDS):                               score += 30
    if any(k in t for k in RANK_KEYWORDS):                               score += 30
    if re.search(r'\d+\s*[%x]|\d[\d,]+', t):                            score += 25
    if re.search(r'(excellence|honor|top|best|promoted)', t):            score += 15
    return min(score, 100)


_SCORERS = {
    "Education":    _score_education,
    "Projects":     _score_projects,
    "Skills":       _score_skills,
    "Experience":   _score_experience,
    "Achievements": _score_achievements,
}


def score_sections(resume_text: str) -> tuple:
    scores   = {}
    feedback = {}
    for section, scorer in _SCORERS.items():
        s = scorer(resume_text)
        scores[section]   = s
        feedback[section] = FEEDBACK_TEMPLATES[section][_feedback_level(s)]
    return scores, feedback
