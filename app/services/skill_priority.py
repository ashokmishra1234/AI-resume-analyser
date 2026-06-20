import re

CORE_SKILLS = {
    "python", "java", "javascript", "typescript", "react", "vue", "angular",
    "fastapi", "django", "flask", "node.js", "express", "spring boot",
    "sql", "mysql", "postgresql", "mongodb", "docker", "api", "rest",
}

PREFERRED_SKILLS = {
    "aws", "gcp", "azure", "kubernetes", "git", "ci/cd", "redis",
    "graphql", "microservices", "testing", "pytest", "jest", "linux",
}

EMPHASIS_WORDS = {"required", "must", "mandatory", "essential", "need", "critical", "expertise"}


def prioritize_missing_skills(missing_skills: list, job_description: str) -> list:
    """
    Score each missing skill on three factors:
        1. Frequency in the JD           (0–30 pts)
        2. Appears near emphasis words   (+25 pts)
        3. Skill category                (Core 25 / Preferred 15 / Other 5)

    Labels:  >= 55 → Critical  |  >= 30 → Important  |  else → Nice to Have
    """
    jd_lower = job_description.lower()
    prioritized = []

    for skill in missing_skills:
        skill_lower = skill.lower()
        pts = 0

        # Factor 1: frequency in JD
        freq = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', jd_lower))
        pts += min(freq * 10, 30)

        # Factor 2: appears near an emphasis word (within ~40 chars)
        for word in EMPHASIS_WORDS:
            pattern = word + r'.{0,40}' + re.escape(skill_lower)
            if re.search(pattern, jd_lower):
                pts += 25
                break

        # Factor 3: skill category
        if skill_lower in CORE_SKILLS:
            pts += 25
        elif skill_lower in PREFERRED_SKILLS:
            pts += 15
        else:
            pts += 5

        if pts >= 55:
            priority = "Critical"
        elif pts >= 30:
            priority = "Important"
        else:
            priority = "Nice to Have"

        prioritized.append({"skill": skill, "priority": priority})

    order = {"Critical": 0, "Important": 1, "Nice to Have": 2}
    prioritized.sort(key=lambda x: order[x["priority"]])
    return prioritized
