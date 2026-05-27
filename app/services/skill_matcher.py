SKILLS = [
    "python",
    "fastapi",
    "react",
    "docker",
    "mysql",
    "mongodb",
    "aws",
    "javascript",
    "machine learning",
    "html",
    "css"
]

def match_skills(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matched = []
    missing = []

    for skill in SKILLS:
        if skill in job_description:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing
