def calculate_ats_score(matched_skills, missing_skills):

    total = len(matched_skills) + len(missing_skills)

    if total == 0:
        return 0

    score = (len(matched_skills) / total) * 100

    return round(score)
