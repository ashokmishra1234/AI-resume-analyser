def basic_resume_analysis(matched_skills, missing_skills):
    """
    Fallback analysis when LLM API fails.
    Provides rule-based analysis using matched and missing skills.
    
    Args:
        matched_skills (list): Skills found in both resume and job description
        missing_skills (list): Skills in job description but not in resume
    
    Returns:
        dict: Analysis with summary and suggestions
    """
    
    # Generate Professional Summary
    if len(matched_skills) > 0:
        summary = f"Your resume demonstrates strong experience with {len(matched_skills)} key technologies. "
        if len(missing_skills) > 0:
            summary += f"However, you lack experience in {len(missing_skills)} important areas that the job requires."
        else:
            summary += "You appear to have all the required skills for this position!"
    else:
        summary = f"Your resume lacks experience in {len(missing_skills)} critical areas required for this role."
    
    # Generate Suggestions
    suggestions = []
    
    # Suggestion based on missing skills
    if len(missing_skills) > 0:
        top_missing = missing_skills[:3]
        skills_text = ", ".join(top_missing)
        suggestions.append(f"Learn and gain experience with: {skills_text}")
    
    # Suggestion based on matched skills
    if len(matched_skills) > 0:
        top_matched = matched_skills[:3]
        skills_text = ", ".join(top_matched)
        suggestions.append(f"Highlight your expertise in {skills_text} in your resume summary")
    
    # General suggestions
    if len(matched_skills) / (len(matched_skills) + len(missing_skills)) > 0.7:
        suggestions.append("You're a strong candidate! Focus on improving the missing skills.")
    else:
        suggestions.append("Consider gaining more experience in the missing technologies before applying.")
    
    suggestions.append("Add more projects and achievements to demonstrate your practical expertise.")
    suggestions.append("Ensure your resume clearly shows impact and results in your previous work.")
    
    # Combine all into summary text
    full_summary = f"""Professional Summary:
{summary}

Strengths:
- You have experience with {len(matched_skills)} required technologies
- Your matched skills include: {', '.join(matched_skills) if matched_skills else 'None'}
- Your resume appears relevant to the position

Weaknesses:
- Missing {len(missing_skills)} important technologies
- Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}
- Consider upskilling in these areas

Suggestions:
- {chr(10).join(['- ' + s for s in suggestions])}"""
    
    return {
        "summary": full_summary,
        "suggestions": suggestions
    }
