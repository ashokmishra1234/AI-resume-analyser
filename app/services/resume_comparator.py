def compare_resumes(resume1_score, resume2_score):
    """
    Compare two resumes based on their ATS scores.
    
    Args:
        resume1_score (int): ATS score of first resume (0-100)
        resume2_score (int): ATS score of second resume (0-100)
    
    Returns:
        dict: Comparison result with winner and scores
    """
    
    if resume1_score > resume2_score:
        winner = "Resume 1"
    elif resume2_score > resume1_score:
        winner = "Resume 2"
    else:
        winner = "Tie"
    
    return {
        "resume1_score": resume1_score,
        "resume2_score": resume2_score,
        "winner": winner,
        "difference": round(abs(resume1_score - resume2_score), 2)
    }
