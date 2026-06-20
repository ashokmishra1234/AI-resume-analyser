import re
import pdfplumber


def extract_resume_text(file):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_and_strip_name(resume_text: str) -> tuple:
    """
    Extract candidate name from the top of the resume, then replace every
    occurrence with 'the candidate' so the LLM never sees the real name.

    Returns (cleaned_text, candidate_name).
    Name detection: checks first 5 lines for a 2-4 word all-alpha string.
    """
    lines = resume_text.strip().split('\n')
    candidate_name = ""

    for line in lines[:5]:
        line = line.strip()
        # 2-4 capitalised words, no digits or punctuation, min length 4
        if re.match(r'^[A-Za-z]+(?: [A-Za-z]+){1,3}$', line) and len(line) > 3:
            candidate_name = line
            break

    if candidate_name:
        cleaned = resume_text.replace(candidate_name, "the candidate")
    else:
        cleaned = resume_text

    return cleaned, candidate_name
