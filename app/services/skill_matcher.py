import re

# Aliases that should be treated as the canonical skill name
NORMALIZATIONS = {
    "js":        "javascript",
    "ts":        "typescript",
    "node":      "node.js",
    "nodejs":    "node.js",
    "reactjs":   "react",
    "react.js":  "react",
    "vue.js":    "vue",
    "vuejs":     "vue",
    "next.js":   "nextjs",
    "nuxt.js":   "nuxt",
    "postgres":  "postgresql",
    "pg":        "postgresql",
    "mongo":     "mongodb",
    "k8s":       "kubernetes",
    "ml":        "machine learning",
}

# Skills that should be treated as interchangeable during matching.
# Key = canonical name (must be in ALL_SKILLS), value = list of synonyms to check in text.
SKILL_GROUPS = {
    "react":            ["react", "reactjs", "react.js"],
    "vue":              ["vue", "vue.js", "vuejs"],
    "node.js":          ["node.js", "nodejs", "node", "express"],
    "nextjs":           ["nextjs", "next.js", "next js"],
    "javascript":       ["javascript", "js"],
    "typescript":       ["typescript", "ts"],
    "postgresql":       ["postgresql", "postgres", "pg"],
    "mongodb":          ["mongodb", "mongo"],
    "kubernetes":       ["kubernetes", "k8s"],
    "machine learning": ["machine learning", "ml"],
    "aws":              ["aws", "amazon web services"],
    "gcp":              ["gcp", "google cloud platform", "google cloud"],
    "sql":              ["sql", "mysql", "postgresql", "sqlite"],
    "git":              ["git", "github", "gitlab"],
    "ci/cd":            ["ci/cd", "github actions", "jenkins", "gitlab ci", "circleci", "circle ci"],
    "docker":           ["docker", "containerization", "containers"],
}

# Full catalog of skills we scan for in the job description
ALL_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "php", "ruby",
    # Frontend
    "react", "vue", "angular", "svelte", "nextjs", "nuxt", "html", "css",
    "tailwind", "bootstrap",
    # Backend frameworks
    "fastapi", "django", "flask", "express", "node.js", "spring boot", "laravel", "rails",
    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "redis", "cassandra", "dynamodb", "sql",
    # Cloud
    "aws", "gcp", "azure",
    # DevOps / infra
    "docker", "kubernetes", "terraform", "linux", "ci/cd",
    # Tools
    "git",
    # API / architecture
    "rest", "graphql", "microservices",
    # AI / ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    # Testing
    "pytest", "jest", "selenium",
]


def normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    return NORMALIZATIONS.get(s, s)


def skill_in_text(skill: str, text_lower: str) -> bool:
    """
    Return True if the skill (or any known synonym) appears in text.
    Uses word boundaries to avoid false matches like 'ml' inside 'html'.
    """
    normalized = normalize_skill(skill)

    # Direct word-boundary match on the canonical form
    if re.search(r'(?<![a-z0-9])' + re.escape(normalized) + r'(?![a-z0-9])', text_lower):
        return True

    # Synonym / alias match via SKILL_GROUPS
    for canonical, synonyms in SKILL_GROUPS.items():
        if normalized == canonical or normalized in synonyms:
            for synonym in synonyms:
                pattern = r'(?<![a-z0-9])' + re.escape(synonym) + r'(?![a-z0-9])'
                if re.search(pattern, text_lower):
                    return True
            break

    return False


def match_skills(resume_text: str, job_description: str) -> tuple:
    """
    Scan ALL_SKILLS catalog against the JD to find required skills,
    then check each against the resume (with synonym expansion).

    Returns (matched_skills, missing_skills).
    """
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    matched = []
    missing = []
    seen = set()

    for skill in ALL_SKILLS:
        if skill in seen:
            continue
        if skill_in_text(skill, jd_lower):       # JD requires this skill
            seen.add(skill)
            if skill_in_text(skill, resume_lower):  # resume has it (or a synonym)
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing
