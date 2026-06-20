"""
Generate two PDFs for AI Resume Analyser backend:
  1. AI_Resume_Analyser_Study_Guide.pdf   — detailed file-by-file explanations
  2. AI_Resume_Analyser_Quick_Revision.pdf — interview prep cheat sheet

Run: python generate_pdfs.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Preformatted, HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm

# ── colour palette ─────────────────────────────────────────────────────────────
BLUE_DARK  = colors.HexColor('#1e3a8a')
BLUE_MED   = colors.HexColor('#1d4ed8')
BLUE_LIGHT = colors.HexColor('#2563eb')
GRAY_DARK  = colors.HexColor('#1f2937')
GRAY_MED   = colors.HexColor('#374151')
GRAY_LIGHT = colors.HexColor('#6b7280')
RED        = colors.HexColor('#dc2626')
GREEN      = colors.HexColor('#166534')
CODE_BG    = colors.HexColor('#f1f5f9')
CODE_BORDER= colors.HexColor('#cbd5e1')


def make_styles():
    return {
        'cover_title': ParagraphStyle('cover_title', fontName='Helvetica-Bold',
            fontSize=26, textColor=BLUE_DARK, alignment=TA_CENTER, spaceAfter=10),
        'cover_sub': ParagraphStyle('cover_sub', fontName='Helvetica',
            fontSize=14, textColor=GRAY_MED, alignment=TA_CENTER, spaceAfter=6),
        'note': ParagraphStyle('note', fontName='Helvetica-Oblique',
            fontSize=9, textColor=GRAY_LIGHT, spaceAfter=4, leftIndent=10),
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold',
            fontSize=16, textColor=BLUE_DARK, spaceBefore=14, spaceAfter=6),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold',
            fontSize=13, textColor=BLUE_MED, spaceBefore=10, spaceAfter=5),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold',
            fontSize=11, textColor=BLUE_LIGHT, spaceBefore=7, spaceAfter=3),
        'body': ParagraphStyle('body', fontName='Helvetica',
            fontSize=10, leading=15, spaceAfter=5, textColor=GRAY_DARK),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica',
            fontSize=10, leading=14, spaceAfter=4,
            leftIndent=18, textColor=GRAY_MED),
        'q': ParagraphStyle('q', fontName='Helvetica-Bold',
            fontSize=10, textColor=RED, spaceBefore=7, spaceAfter=2),
        'a': ParagraphStyle('a', fontName='Helvetica',
            fontSize=10, leading=14, spaceAfter=5,
            leftIndent=14, textColor=GREEN),
        'code': ParagraphStyle('code', fontName='Courier',
            fontSize=8, leading=11, spaceAfter=6, spaceBefore=3,
            leftIndent=8, backColor=CODE_BG),
    }


# ── helper builders ─────────────────────────────────────────────────────────────

def e(t):
    """Escape text for Paragraph XML parser."""
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def T(s, st, text, style='body'):
    s.append(Paragraph(e(text), st[style]))


def H1(s, st, text):
    s.append(Spacer(1, 0.2 * cm))
    s.append(HRFlowable(width='100%', thickness=2, color=BLUE_DARK, spaceAfter=4))
    s.append(Paragraph(e(text), st['h1']))


def H2(s, st, text):
    s.append(Paragraph(e(text), st['h2']))


def H3(s, st, text):
    s.append(Paragraph(e(text), st['h3']))


def Code(s, code_text):
    code_style = ParagraphStyle('_code', fontName='Courier', fontSize=8,
                                leading=11, spaceAfter=6, spaceBefore=3,
                                leftIndent=8, backColor=CODE_BG)
    s.append(Preformatted(code_text, code_style))


def QA(s, st, q, a):
    s.append(Paragraph('Q: ' + e(q), st['q']))
    s.append(Paragraph('A: ' + e(a), st['a']))


def B(s, st, text):
    s.append(Paragraph('•  ' + e(text), st['bullet']))


def HR(s):
    s.append(Spacer(1, 0.15 * cm))
    s.append(HRFlowable(width='100%', thickness=0.5,
                        color=colors.HexColor('#e2e8f0')))
    s.append(Spacer(1, 0.15 * cm))


# ══════════════════════════════════════════════════════════════════════════════
#  DETAILED STUDY GUIDE
# ══════════════════════════════════════════════════════════════════════════════

def build_detailed(st):
    s = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    s.append(Spacer(1, 5 * cm))
    s.append(Paragraph('AI Resume Analyser', st['cover_title']))
    s.append(Paragraph('Backend Architecture — Complete Study Guide', st['cover_sub']))
    s.append(Spacer(1, 1 * cm))
    s.append(Paragraph('All 12 backend files + main.py  |  Line-by-line explanations', st['cover_sub']))
    s.append(Paragraph('Interview Q&As  |  Real-world scenarios  |  Who calls what', st['note']))
    s.append(PageBreak())

    # ── Architecture flow ─────────────────────────────────────────────────────
    H1(s, st, 'Backend Flow — Resume Analysis')
    T(s, st, 'When a user uploads a resume PDF and job description, the request travels '
             'through these layers in strict order:')
    Code(s, """\
BROWSER  POST /resume/analyze  (multipart/form-data: PDF file + JD text)
    |
main.py        CORSMiddleware validates origin; routing table dispatches
    |
routes_resume  Depends(get_current_user) -> validates JWT
               Depends(get_db)           -> opens DB session
               extract_resume_text(UploadFile) -> raw string
               run_full_analysis(resume_text, job_description) -> ctx
    |
analysis_pipeline.py  11 steps in strict order:
  Step 1  extract_and_strip_name()         -> cleaned_text, candidate_name
  Step 2  match_skills()                   -> matched_skills, missing_skills
  Step 3  score_sections()                 -> section_scores, section_feedback  (BEFORE Step 5)
  Step 4  generate_resume_checklist()      -> resume_audit                       (BEFORE Step 6)
  Step 5  calculate_ats_score()            -> ats_score      (needs Step 3)
  Step 6  calculate_recruiter_fit_score()  -> recruiter_fit  (needs Steps 3+4)
  Step 7  generate_resume_verdict()        -> verdict, interview_chance, fit_level
  Step 8  prioritize_missing_skills()      -> prioritized_missing_skills
  Step 9  generate_recommendations()       -> recommendations
  Step 10 _build_structured_facts()        -> name-free dict for LLM
  Step 11 generate_ai_feedback_from_facts()-> ai_feedback  (only network call)
    |
routes_resume  build result dict from ctx
               db.add(Analysis(...)); db.commit()
               return result
    |
BROWSER  HTTP 200 JSON\
""")
    s.append(PageBreak())

    # ── FILE 1 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 1 of 12  —  app/models/analysis_context.py')
    T(s, st, 'NEW file. A single Python dataclass that flows through all 11 pipeline steps. '
             'Before this, each service module held its own data copy — inconsistencies were common. '
             'Now one object is created at pipeline start and mutated by each step.')
    T(s, st, 'Called from: analysis_pipeline.py — ctx = ResumeAnalysisContext(raw_resume_text=..., raw_job_description=...)')
    H2(s, st, 'Key Code')
    Code(s, """\
from dataclasses import dataclass, field

@dataclass
class ResumeAnalysisContext:
    raw_resume_text: str           # required — original PDF text
    raw_job_description: str       # required — original JD

    cleaned_resume_text: str = ""  # after name strip (Step 1)
    candidate_name: str = ""       # extracted name — NEVER sent to LLM

    matched_skills: list = field(default_factory=list)
    missing_skills: list = field(default_factory=list)

    ats_score: float = 0.0
    recruiter_fit_score: float = 0.0
    resume_verdict: str = ""
    interview_chance: str = ""
    fit_level: str = ""

    section_scores: dict = field(default_factory=dict)
    section_feedback: dict = field(default_factory=dict)
    prioritized_missing_skills: list = field(default_factory=list)
    resume_audit: dict = field(default_factory=dict)
    recommendations: list = field(default_factory=list)

    structured_facts: dict = field(default_factory=dict)   # name-free snapshot for LLM
    ai_feedback: dict = field(default_factory=dict)        # LLM output\
""")
    H2(s, st, 'Key Concepts')
    B(s, st, '@dataclass: auto-generates __init__, __repr__, __eq__ from field annotations. '
             'No manual __init__ needed for 17 fields.')
    B(s, st, 'field(default_factory=list): mutable defaults (list, dict) MUST use default_factory. '
             'Using = [] directly is a Python bug — all instances share the same list object.')
    B(s, st, 'str = "" and float = 0.0: immutable defaults are safe to set directly. '
             'Each instance gets its own copy automatically.')
    B(s, st, 'First two fields have NO default — they are required positional arguments '
             'and must be supplied when creating the object.')
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why use field(default_factory=list) instead of = []?',
       'Default values are evaluated once at class definition time. Writing matched_skills: list = [] '
       'means ALL instances share the same list. Appending to one instance appends to all. '
       'field(default_factory=list) calls list() fresh for each new instance, giving each its own list.')
    QA(s, st, 'What does @dataclass save you from writing?',
       '__init__ with all 17 parameters, __repr__ for printing, __eq__ for equality comparison. '
       'Without @dataclass those would be ~50 lines of boilerplate. The decorator generates all three.')
    QA(s, st, 'What is the difference between a dataclass and a regular class?',
       'A regular class needs a manual __init__. A dataclass generates it from field annotations. '
       'Dataclasses are ideal for data containers. Regular classes are better when you need '
       'complex inheritance, custom initialization, or significant method logic.')
    s.append(PageBreak())

    # ── FILE 2 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 2 of 12  —  app/services/resume_parser.py')
    T(s, st, 'UPDATED. extract_resume_text() is unchanged — reads all pages from a PDF via pdfplumber. '
             'New function extract_and_strip_name() detects the candidate name in the first 5 lines '
             'using regex and replaces every occurrence with "the candidate" before the LLM sees it.')
    T(s, st, 'Called from: routes_resume.py calls extract_resume_text(). '
             'analysis_pipeline.py Step 1 calls extract_and_strip_name().')
    H2(s, st, 'Key Code')
    Code(s, """\
import re, pdfplumber

def extract_resume_text(file):
    text = ""
    with pdfplumber.open(file.file) as pdf:   # file.file = SpooledTemporaryFile
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_and_strip_name(resume_text: str) -> tuple:
    lines = resume_text.strip().split('\\n')
    candidate_name = ""
    for line in lines[:5]:                    # scan first 5 lines only
        line = line.strip()
        # 2-4 capitalised words, letters only, min length 4
        if re.match(r'^[A-Za-z]+(?: [A-Za-z]+){1,3}$', line) and len(line) > 3:
            candidate_name = line
            break
    if candidate_name:
        cleaned = resume_text.replace(candidate_name, "the candidate")
    else:
        cleaned = resume_text
    return cleaned, candidate_name            # tuple unpacking by caller\
""")
    H2(s, st, 'Key Concepts')
    B(s, st, 'file.file: UploadFile.file is the underlying SpooledTemporaryFile (binary stream). '
             'pdfplumber.open() accepts any file-like object with a .read() method.')
    B(s, st, 're.match(r"^[A-Za-z]+(?: [A-Za-z]+){1,3}$"): ^ anchors to start, $ to end. '
             '{1,3} means 1-3 repetitions of (space + word). Matches 2-4 all-letter words.')
    B(s, st, 'lines[:5]: slice of first 5 lines. Names appear at the top of resumes. '
             'Scanning all lines risks false positives from project names or company names.')
    B(s, st, 'return cleaned, candidate_name: Python returns a tuple. '
             'Caller unpacks with: cleaned_text, name = extract_and_strip_name(text)')
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What is file.file in FastAPI UploadFile?',
       'UploadFile is FastAPI\'s wrapper around uploaded binary data. .file is the raw '
       'SpooledTemporaryFile — lives in memory if small, spills to /tmp if large. '
       'pdfplumber reads it directly without saving to disk first.')
    QA(s, st, 'Why replace name with "the candidate" instead of deleting it?',
       'Deletion creates broken sentences. "John has 3 years experience" becomes '
       '"has 3 years experience" — grammatically wrong. "the candidate has 3 years experience" '
       'is correct and meaningful. The LLM can still understand and respond about the person.')
    QA(s, st, 'Why check only the first 5 lines for a name?',
       'Names appear at the very top of resumes — line 1 or 2. Scanning all lines risks '
       'false positives: a project name like "Task Manager" or a company name like "Google Cloud" '
       'could match the 2-4 word pattern. Limiting to 5 lines keeps it fast and accurate.')
    s.append(PageBreak())

    # ── FILE 3 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 3 of 12  —  app/services/skill_matcher.py')
    T(s, st, 'REWRITTEN. Old version used "if skill in text" — "ml" matched inside "html". '
             'New version uses regex word boundaries, alias normalisation (reactjs->react), '
             'and synonym groups so react/reactjs/react.js are treated as one skill.')
    T(s, st, 'Called from: analysis_pipeline.py Step 2. Also routes_compare.py and legacy ai_analyzer.py.')
    H2(s, st, 'Key Code')
    Code(s, """\
NORMALIZATIONS = {"js": "javascript", "nodejs": "node.js", "reactjs": "react", ...}
SKILL_GROUPS = {
    "react":   ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node", "express"],
}
ALL_SKILLS = ["python", "java", "javascript", "react", ...]  # 50+ skills

def normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    return NORMALIZATIONS.get(s, s)

def skill_in_text(skill: str, text_lower: str) -> bool:
    normalized = normalize_skill(skill)
    # word boundary via negative lookaround (handles node.js, ci/cd)
    if re.search(r'(?<![a-z0-9])' + re.escape(normalized) + r'(?![a-z0-9])', text_lower):
        return True
    # check all synonyms in the skill's group
    for canonical, synonyms in SKILL_GROUPS.items():
        if normalized == canonical or normalized in synonyms:
            for syn in synonyms:
                if re.search(r'(?<![a-z0-9])' + re.escape(syn) + r'(?![a-z0-9])', text_lower):
                    return True
            break
    return False

def match_skills(resume_text: str, job_description: str) -> tuple:
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    matched, missing, seen = [], [], set()   # seen = set for O(1) dedup
    for skill in ALL_SKILLS:
        if skill in seen: continue
        if skill_in_text(skill, jd_lower):   # skill required by JD?
            seen.add(skill)
            if skill_in_text(skill, resume_lower):
                matched.append(skill)
            else:
                missing.append(skill)
    return matched, missing\
""")
    H2(s, st, 'Key Concepts')
    B(s, st, '(?<![a-z0-9]): negative lookbehind — match only if the character BEFORE the skill '
             'is NOT a letter or digit. Prevents "ml" matching inside "html".')
    B(s, st, '(?![a-z0-9]): negative lookahead — same for the character AFTER the skill. '
             'Together they act as word boundary detection without \\b.')
    B(s, st, 're.escape(skill): escapes special regex characters in skill names like "node.js" '
             '(dot becomes \\.) or "c++" (plus becomes \\+). Without it, "." means "any character".')
    B(s, st, 'seen set: set membership is O(1) vs O(n) for list. '
             'Prevents double-counting when normalisation maps multiple aliases to same skill.')
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why use negative lookbehind/lookahead instead of \\b word boundaries?',
       '\\b considers "." a non-word character, so node.js breaks at the dot — \\b would '
       'match "node" and "js" separately. Negative lookbehind/lookahead checks that '
       'surrounding characters are not [a-z0-9], correctly treating node.js as one unit '
       'and preventing "ml" from matching inside "html".')
    QA(s, st, 'What does re.escape() do and why is it necessary?',
       're.escape() adds backslashes before special regex characters: . + * ? ( ) [ ] { } ^ $ | \\ '
       'Without it, skill names containing special chars (node.js, c++, ci/cd) would be '
       'interpreted as regex patterns — "." matches any character, "+" means one-or-more.')
    QA(s, st, 'set vs list for the "seen" variable — what is the difference?',
       '"x in seen" on a set is O(1) — hash lookup. On a list it is O(n) — scans every element. '
       'With 50+ skills, the set version is significantly faster. Sets also semantically '
       'express "unique membership" which is exactly what deduplication needs.')
    s.append(PageBreak())

    # ── FILE 4 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 4 of 12  —  app/services/ats_score.py')
    T(s, st, 'REWRITTEN. Old version had one function returning skill-ratio only. '
             'New version has three functions: weighted ATS (6 factors), '
             'recruiter fit (6 factors), interview probability (combined label).')
    T(s, st, 'Called from: analysis_pipeline.py Steps 5 and 6. '
             'compute_interview_probability also imported by resume_verdict.py. '
             'calculate_ats_score also used in routes_compare.py.')
    H2(s, st, 'Weighted ATS Formula (40/20/15/10/10/5)')
    Code(s, """\
def calculate_ats_score(matched_skills, missing_skills, section_scores=None) -> float:
    total = len(matched_skills) + len(missing_skills)
    skill_score = (len(matched_skills) / max(total, 1)) * 100  # max() prevents / 0

    if not section_scores:                 # fallback: skill-only when sections unavailable
        return round(skill_score, 1)

    projects_score     = section_scores.get("Projects", 0)
    experience_score   = section_scores.get("Experience", 0)
    education_score    = section_scores.get("Education", 0)
    achievements_score = section_scores.get("Achievements", 0)

    required = ["Education","Projects","Skills","Experience","Achievements"]
    present = sum(1 for sec in required if section_scores.get(sec, 0) > 20)
    completeness_score = (present / len(required)) * 100

    weighted = (
        skill_score        * 0.40 +   # 40% — skill keyword match
        projects_score     * 0.20 +   # 20% — project quality
        experience_score   * 0.15 +   # 15% — work experience
        education_score    * 0.10 +   # 10% — education
        achievements_score * 0.10 +   # 10% — certifications/awards
        completeness_score * 0.05     #  5% — all sections present
    )
    return round(weighted, 1)

def compute_interview_probability(ats_score, recruiter_fit_score) -> str:
    combined = (ats_score * 0.4) + (recruiter_fit_score * 0.6)
    if combined >= 75: return "Very High"
    if combined >= 60: return "High"
    if combined >= 45: return "Medium"
    return "Low"\
""")
    H2(s, st, 'Recruiter Fit Score — 6 Factors (max 100)')
    B(s, st, 'Matched skill count: 3 pts each, max 25 pts')
    B(s, st, 'Action verbs (built/developed/reduced/optimized...): 2 pts each, max 20 pts')
    B(s, st, 'GitHub Profile present: 10 pts. Deployment Links: 5 pts')
    B(s, st, 'Quantified metrics (30%, 10x, 5000 users): 7 pts each, max 20 pts')
    B(s, st, 'Education section score >= 40: 10 pts')
    B(s, st, 'Word count 300-800: 10 pts; 200-300 or 800-1000: 5 pts')
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What does max(total, 1) protect against?',
       'Division by zero. If both matched and missing are empty, total = 0. '
       'len(matched) / 0 raises ZeroDivisionError. max(total, 1) returns 1 when total is 0, '
       'making the division safe: 0/1 = 0%.')
    QA(s, st, 'Why does section_scores default to None instead of {}?',
       'None lets the "if not section_scores" check distinguish "caller passed no sections" '
       'from "caller passed an empty dict". Both {} and None are falsy, but semantically '
       'None means "not provided" while {} means "provided but empty". The function uses '
       'None as the sentinel for the skill-only fallback path.')
    QA(s, st, 'Why weight recruiter_fit 60% vs ats_score 40% in interview probability?',
       'ATS systems filter automatically — keyword matching. But actual hiring is done by humans. '
       'A candidate with great soft signals (GitHub, metrics, action verbs) who slightly misses '
       'keyword matching is still a strong hire. The 0.6 weight reflects that human judgment '
       'matters more than automated keyword scanning.')
    s.append(PageBreak())

    # ── FILE 5 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 5 of 12  —  app/services/resume_verdict.py')
    T(s, st, 'REWRITTEN. Now takes both ats_score and recruiter_fit_score. '
             'Imports compute_interview_probability from ats_score.py — single source of truth. '
             'Returns a dict with verdict label, interview chance, and fit level percentage.')
    T(s, st, 'Called from: analysis_pipeline.py Step 7.')
    H2(s, st, 'Key Code')
    Code(s, """\
from app.services.ats_score import compute_interview_probability

def generate_resume_verdict(ats_score, recruiter_fit_score, matched_skills, missing_skills) -> dict:
    # Verdict based on ATS score only (not recruiter fit)
    if   ats_score >= 80: verdict = "Strong Candidate"
    elif ats_score >= 60: verdict = "Good Candidate"
    elif ats_score >= 40: verdict = "Average Candidate"
    else:                 verdict = "Needs Improvement"

    # Interview probability uses combined ATS + recruiter fit
    interview_chance = compute_interview_probability(ats_score, recruiter_fit_score)

    total = len(matched_skills) + len(missing_skills)
    fit_percentage = (len(matched_skills) / max(total, 1)) * 100
    fit_level = f"{round(fit_percentage)}%"    # e.g. "67%"

    return {
        "resume_verdict": verdict,
        "interview_chance": interview_chance,
        "fit_level": fit_level,
        "ats_score": ats_score,
        "recruiter_fit_score": recruiter_fit_score
    }\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why does verdict use only ats_score thresholds and not recruiter_fit?',
       'Verdict labels describe ATS performance — the automated screening stage. '
       'Recruiter fit is a separate dimension shown as interview_chance. '
       'Mixing both into one label would confuse what each number means.')
    QA(s, st, 'What is f"{round(fit_percentage)}%" — explain each part?',
       'f"..." is an f-string — Python string interpolation. The expression inside {} is '
       'evaluated and inserted into the string. round(fit_percentage) rounds to nearest integer. '
       'Result: if fit_percentage = 66.67, the string becomes "67%".')
    s.append(PageBreak())

    # ── FILE 6 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 6 of 12  —  app/services/section_scorer.py')
    T(s, st, 'REWRITTEN. Old version counted occurrences of generic keywords. '
             'New version uses targeted quality rubrics per section — Education checks '
             'degree + college + GPA + year + field of study, not just "education" keyword count. '
             'Returns a tuple: (scores_dict, feedback_dict).')
    T(s, st, 'Called from: analysis_pipeline.py Step 3. Also routes_compare.py (tuple must be unpacked).')
    H2(s, st, 'Dispatch Dictionary Pattern')
    Code(s, """\
_SCORERS = {
    "Education":    _score_education,
    "Projects":     _score_projects,
    "Skills":       _score_skills,
    "Experience":   _score_experience,
    "Achievements": _score_achievements,
}

def _feedback_level(score: int) -> str:
    if score >= 70: return "high"
    if score >= 40: return "medium"
    return "low"

def score_sections(resume_text: str) -> tuple:
    scores, feedback = {}, {}
    for section, scorer in _SCORERS.items():  # dispatch: call right function automatically
        s = scorer(resume_text)
        scores[section]   = s
        feedback[section] = FEEDBACK_TEMPLATES[section][_feedback_level(s)]
    return scores, feedback    # caller unpacks: section_scores, section_feedback = score_sections()\
""")
    H2(s, st, 'Section Rubrics — What Each Scorer Checks')
    B(s, st, 'Education (max 100): degree keyword +30, college keyword +20, '
             'GPA/CGPA number +25, graduation year +15, field of study +10')
    B(s, st, 'Projects (max 100): tech stack variety +30 (5 pts/tech), '
             'github.com link +20, deployment link +20, metrics +20, project count +10')
    B(s, st, 'Skills (max 100): tech keyword count x7, capped at 100')
    B(s, st, 'Experience (max 100): experience/intern keyword +20, '
             'action verbs +35, quantified metrics +25, tech diversity +20')
    B(s, st, 'Achievements (max 100): certification keywords +30, '
             'rank/winner keywords +30, numbers +25, excellence/honor +15')
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What is the dispatch dictionary pattern and why use it over if/elif?',
       '_SCORERS maps section names to functions. score_sections() loops over it calling each. '
       'If/elif would require a new elif for every new section plus changing score_sections(). '
       'With dispatch dict: add _score_new_section() + one dict entry. The loop never changes.')
    QA(s, st, 'What bug in routes_compare.py was caused by score_sections() returning a tuple?',
       'Old code: section_scores = score_sections(text) — stored the whole tuple. '
       'FastAPI serialized it as JSON array [scores_dict, feedback_dict]. '
       'Frontend received array where it expected dict. Object.entries(array) returned indices '
       '["0", "1"]. Rendering {score}% where score was a dict crashed React — blank page. '
       'Fix: section_scores, _ = score_sections(text) — unpack and discard feedback.')
    s.append(PageBreak())

    # ── FILE 7 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 7 of 12  —  app/services/skill_priority.py')
    T(s, st, 'REWRITTEN. Old version returned missing skills as a flat list. '
             'New version assigns Critical / Important / Nice to Have priority to each '
             'missing skill using three scoring factors.')
    T(s, st, 'Called from: analysis_pipeline.py Step 8.')
    H2(s, st, 'Three Scoring Factors')
    Code(s, """\
CORE_SKILLS      = {"python","java","react","fastapi","docker","sql",...}  # set: O(1) lookup
PREFERRED_SKILLS = {"aws","gcp","kubernetes","git","ci/cd",...}
EMPHASIS_WORDS   = {"required","must","mandatory","essential","critical","expertise"}

def prioritize_missing_skills(missing_skills, job_description) -> list:
    jd_lower = job_description.lower()
    prioritized = []
    for skill in missing_skills:
        pts = 0
        skill_lower = skill.lower()

        # Factor 1: JD frequency — how often does the JD mention this skill? (max 30 pts)
        freq = len(re.findall(r'\\b' + re.escape(skill_lower) + r'\\b', jd_lower))
        pts += min(freq * 10, 30)

        # Factor 2: Emphasis word proximity — "required", "must" near the skill? (0 or 25 pts)
        for word in EMPHASIS_WORDS:
            if re.search(word + r'.{0,40}' + re.escape(skill_lower), jd_lower):
                pts += 25
                break   # only add 25 once even if multiple emphasis words match

        # Factor 3: Skill category — core/preferred/other (25/15/5 pts)
        if skill_lower in CORE_SKILLS:           pts += 25
        elif skill_lower in PREFERRED_SKILLS:    pts += 15
        else:                                     pts += 5

        priority = "Critical" if pts >= 55 else "Important" if pts >= 30 else "Nice to Have"
        prioritized.append({"skill": skill, "priority": priority})

    order = {"Critical": 0, "Important": 1, "Nice to Have": 2}
    prioritized.sort(key=lambda x: order[x["priority"]])
    return prioritized\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why use a set for CORE_SKILLS instead of a list?',
       '"python" in CORE_SKILLS on a set is O(1) — instant hash lookup. '
       'On a list it is O(n) — scans every element. This function runs for every missing '
       'skill. With 20+ items in CORE_SKILLS, the set is dramatically faster.')
    QA(s, st, 'What does word + r".{0,40}" + skill do?',
       'It matches the emphasis word followed by up to 40 characters, then the skill name. '
       'Checks if JD says "Python is required" or "required expertise in Python" — within '
       '40 characters of each other. Without .{0,40}, "required" anywhere in the JD would '
       'trigger even if it refers to a different skill entirely.')
    QA(s, st, 'What is lambda x: order[x["priority"]] in the sort call?',
       'sort(key=...) takes a function that extracts a comparison value from each item. '
       'lambda x: order[x["priority"]] is an anonymous function that takes a dict '
       '{"skill": "docker", "priority": "Critical"} and returns order["Critical"] = 0. '
       'Python sorts by these numbers — 0 first, then 1, then 2 — so Critical comes first.')
    s.append(PageBreak())

    # ── FILE 8 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 8 of 12  —  app/services/resume_checklist.py')
    T(s, st, 'UPDATED. Original generate_resume_checklist() is unchanged — audits 11 items '
             '(GitHub, LinkedIn, metrics, education, etc.) into found/missing lists. '
             'New generate_recommendations() added at the bottom — reads audit + section scores + '
             'priorities to produce up to 5 specific, actionable recommendations.')
    T(s, st, 'Called from: analysis_pipeline.py — Step 4 calls generate_resume_checklist(), '
             'Step 9 calls generate_recommendations().')
    H2(s, st, 'Key Code — generate_recommendations()')
    Code(s, """\
def generate_recommendations(resume_audit, section_scores, prioritized_missing_skills) -> list:
    recs = []
    # Convert lists to sets for O(1) lookup
    found_names   = {item["name"] for item in resume_audit.get("found", [])}
    missing_names = {item["name"] for item in resume_audit.get("missing", [])}

    if "GitHub Profile"          in missing_names: recs.append("Add a GitHub profile link...")
    if "Deployment Links"        in missing_names: recs.append("Deploy a project, add live URL...")
    if "Quantified Achievements" in missing_names: recs.append("Add 2-3 metrics: 'reduced load by 30%'...")
    if section_scores.get("Experience", 100) < 40: recs.append("Rewrite with action verbs...")
    if section_scores.get("Projects", 100)   < 40: recs.append("Add 2 end-to-end projects...")
    if "LinkedIn Profile"        in missing_names: recs.append("Add LinkedIn URL...")

    critical = [s["skill"] for s in prioritized_missing_skills if s["priority"] in ("High","Critical")]
    if critical:
        recs.append(f"Build a project using {critical[0]} to close the most critical gap...")

    if section_scores.get("Achievements", 100) < 40: recs.append("Add certifications or awards...")

    return recs[:5]   # cap at 5 — cognitive load\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why does section_scores.get("Experience", 100) default to 100?',
       'If the "Experience" key is missing, we assume the section is fine and should NOT trigger '
       'the recommendation. Defaulting to 0 would add the action verb recommendation for every '
       'resume where section scoring skipped Experience — a false positive. '
       '100 makes the "< 40" check fail safely when data is absent.')
    QA(s, st, 'Why cap at recs[:5]?',
       'Cognitive load — psychology research shows people act on 3-5 items. '
       'More than 5 causes decision paralysis and the candidate acts on none. '
       'Conditions are checked in priority order so only the most impactful ones make the cut.')
    QA(s, st, 'Why does this function take three parameters instead of raw resume text?',
       'Because all three inputs were already computed by earlier pipeline steps (3, 4, 8). '
       'Re-reading the resume would duplicate work. This function does only decision logic — '
       'reading already-computed facts and deciding which recommendations apply. '
       'This is the pipeline pattern\'s core benefit: no re-computation.')
    s.append(PageBreak())

    # ── FILE 9 ────────────────────────────────────────────────────────────────
    H1(s, st, 'File 9 of 12  —  app/services/ai_analyzer.py')
    T(s, st, 'REWRITTEN. Old version sent raw resume text to LLM — could expose name and hallucinate. '
             'New version: SYSTEM_PROMPT forbids name usage and hallucination; '
             'primary function receives only pre-computed structured facts (no raw text, no name); '
             'three-level fallback chain guarantees the endpoint never crashes.')
    T(s, st, 'Called from: analysis_pipeline.py Step 11.')
    H2(s, st, 'SYSTEM_PROMPT + Three-Level Fallback Chain')
    Code(s, """\
SYSTEM_PROMPT = \"\"\"You are a professional resume analyst.
CRITICAL RULES:
1. NEVER use any person name. Always say 'the candidate'.
2. Only generate feedback supported by the structured data you receive.
3. Never invent strengths — only from matched_skills or section score >= 70.
4. Never invent weaknesses — only from critical_missing_skills or score < 40.
5. Write in third person only. Never use 'you' or 'your'.\"\"\"

# Level 1: LLM returns valid JSON
def generate_ai_feedback_from_facts(structured_facts: dict) -> dict:
    try:
        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"...ANALYSIS DATA: {json.dumps(structured_facts)}")
        ])
        parsed = parse_structured_response(response.content)
        if parsed and all(k in parsed for k in required_keys):
            return parsed               # Level 1: clean JSON from LLM

        return _parse_text_response(response.content)   # Level 2: LLM returned plain text

    except Exception:
        return generate_fallback_from_facts(structured_facts)   # Level 3: rule-based fallback

# parse_structured_response — extracts JSON from LLM response (may include markdown wrapping)
def parse_structured_response(content: str) -> dict | None:
    try:
        return json.loads(content)         # Try 1: pure JSON
    except json.JSONDecodeError:
        start = content.find("{")
        end   = content.rfind("}") + 1     # rfind + 1 to include closing }
        if start != -1 and end > start:
            return json.loads(content[start:end])   # Try 2: extract from markdown wrapper
    return None\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why is llm = ChatGroq(...) at module level?',
       'Creating the client inside the function re-initializes the HTTP connection on every call. '
       'At module level it is created once when Python imports the file and reused across all '
       'requests. For a function called on every resume upload, per-call initialization adds '
       'significant latency and memory allocation overhead.')
    QA(s, st, 'What is the difference between SystemMessage and HumanMessage?',
       'SystemMessage sets the LLM persona and hard rules — read before the conversation. '
       'HumanMessage is the actual user request. System messages set constraints the model '
       'prioritizes. SYSTEM_PROMPT forbids name usage even if the human message accidentally '
       'includes one (e.g., in the job_title_hint snippet).')
    QA(s, st, 'Why does rfind("}") need + 1?',
       'rfind returns the index of the last }. Python slicing content[start:end] excludes end. '
       'Without +1, the slice stops before the closing }, making the JSON invalid. '
       '+1 makes the slice include that final character.')
    s.append(PageBreak())

    # ── FILE 10 ───────────────────────────────────────────────────────────────
    H1(s, st, 'File 10 of 12  —  app/services/analysis_pipeline.py')
    T(s, st, 'NEW file. The orchestrator. Calls all service functions in correct order '
             'through a single shared ResumeAnalysisContext. One public function '
             'run_full_analysis() is all the route handler needs to call.')
    T(s, st, 'Called from: routes_resume.py — ctx = run_full_analysis(resume_text, job_description)')
    H2(s, st, 'Step Order and Why It Matters')
    Code(s, """\
def run_full_analysis(resume_text: str, job_description: str) -> ResumeAnalysisContext:
    ctx = ResumeAnalysisContext(raw_resume_text=resume_text, raw_job_description=job_description)

    # Step 1: name strip — cleaned_text used by ALL subsequent steps
    cleaned_text, candidate_name = extract_and_strip_name(resume_text)
    ctx.cleaned_resume_text = cleaned_text
    ctx.candidate_name = candidate_name

    # Step 2: skills
    matched, missing = match_skills(cleaned_text, job_description)
    ctx.matched_skills = matched;  ctx.missing_skills = missing

    # Step 3: MUST be before Step 5 — section_scores feeds weighted ATS formula
    section_scores, section_feedback = score_sections(cleaned_text)
    ctx.section_scores = section_scores;  ctx.section_feedback = section_feedback

    # Step 4: MUST be before Step 6 — resume_audit feeds recruiter fit GitHub/metrics checks
    checklist = generate_resume_checklist(cleaned_text, job_description)
    ctx.resume_audit = checklist.get("resume_audit", {"found": [], "missing": []})

    # Step 5: weighted ATS (needs section_scores from Step 3)
    ctx.ats_score = calculate_ats_score(matched, missing, section_scores)

    # Step 6: recruiter fit (needs section_scores from Step 3 + audit from Step 4)
    ctx.recruiter_fit_score = calculate_recruiter_fit_score(
        cleaned_text, matched, section_scores, ctx.resume_audit)

    # Step 7: verdict + interview chance (needs Steps 5+6)
    verdict = generate_resume_verdict(ctx.ats_score, ctx.recruiter_fit_score, matched, missing)
    ctx.resume_verdict = verdict["resume_verdict"]
    ctx.interview_chance = verdict["interview_chance"]
    ctx.fit_level = verdict["fit_level"]

    # Steps 8-9: priorities and recommendations
    ctx.prioritized_missing_skills = prioritize_missing_skills(missing, job_description)
    ctx.recommendations = generate_recommendations(ctx.resume_audit, ctx.section_scores,
                                                    ctx.prioritized_missing_skills)

    # Step 10: build name-free snapshot for LLM
    ctx.structured_facts = _build_structured_facts(ctx)

    # Step 11: LLM call — last, because needs all above; only network call in pipeline
    ctx.ai_feedback = generate_ai_feedback_from_facts(ctx.structured_facts)

    return ctx\
""")
    H2(s, st, '_build_structured_facts — What the LLM Receives')
    Code(s, """\
def _build_structured_facts(ctx):             # _ prefix = private to this module
    found_names = {item["name"] for item in ctx.resume_audit.get("found", [])}
    return {
        "ats_score":              ctx.ats_score,
        "recruiter_fit_score":    ctx.recruiter_fit_score,
        "resume_verdict":         ctx.resume_verdict,
        "matched_skills":         ctx.matched_skills,
        "critical_missing_skills":[...],           # filtered from prioritized list
        "section_scores":         ctx.section_scores,
        "has_github":  "GitHub Profile"          in found_names,  # boolean, not list
        "has_metrics": "Quantified Achievements" in found_names,
        "job_title_hint": ctx.raw_job_description[:100],
        # ABSENT: raw_resume_text, cleaned_resume_text, candidate_name
    }\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'Why must Step 3 (section scoring) run before Step 5 (ATS)?',
       'calculate_ats_score() takes section_scores as its third argument for the weighted formula '
       '(projects 20%, experience 15%, education 10%...). If Step 5 ran before Step 3, '
       'section_scores would be an empty dict and the formula would silently fall back to '
       'skill-only scoring — wrong result, no error, no warning.')
    QA(s, st, 'Why is the LLM call (Step 11) the last step?',
       'It needs facts from all previous steps. If it were earlier, those facts wouldn\'t exist yet. '
       'Also: if the LLM fails, all deterministic scores (ATS, sections, verdict, priorities, '
       'recommendations) are already computed and returned to the user. Running LLM first would '
       'mean an API failure loses all results.')
    QA(s, st, 'What does the _ prefix on _build_structured_facts mean?',
       'Python convention for "private to this module." Not enforced — just signals to other '
       'developers "do not import or call this from outside." The function is an internal '
       'implementation detail of the pipeline, not part of its public interface.')
    s.append(PageBreak())

    # ── FILE 11 ───────────────────────────────────────────────────────────────
    H1(s, st, 'File 11 of 12  —  app/api/routes_resume.py')
    T(s, st, 'UPDATED. Old version had 10+ service calls inline. New version has exactly two: '
             'extract_resume_text() then run_full_analysis(). '
             'Added recruiter_fit_score, recruiter_recommendations to response. '
             'Added DB saving of every analysis per user.')
    H2(s, st, 'Key Code')
    Code(s, """\
@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),           # binary file from multipart form
    job_description: str = Form(...),          # text field from same multipart form
    current_user: dict = Depends(get_current_user),  # JWT validated before route runs
    db: Session = Depends(get_db)             # DB session opened + closed automatically
):
    # 1. Extract text from PDF (HTTP layer concern)
    resume_text = extract_resume_text(resume)

    # 2. Run all 11 pipeline steps (single call)
    ctx = run_full_analysis(resume_text, job_description)

    # 3. Build response dict from ctx (flatten nested ai_feedback)
    result = {
        "ats_score":             ctx.ats_score,
        "recruiter_fit_score":   ctx.recruiter_fit_score,
        "candidate_overview":    ctx.ai_feedback.get("candidate_overview", ""),
        "strengths":             ctx.ai_feedback.get("strengths", []),
        "improvement_areas":     ctx.ai_feedback.get("improvement_areas", []),
        "recommended_actions":   ctx.ai_feedback.get("recommended_actions", []),
        "resume_audit":          ctx.resume_audit,
        "recruiter_recommendations": ctx.recommendations,
        # ... + matched_skills, missing_skills, section_scores, section_feedback,
        #       resume_verdict, interview_chance, fit_level, skill_priorities
    }

    # 4. Save to DB (Text column stores JSON string)
    db.add(Analysis(
        user_id=int(current_user["sub"]),   # JWT "sub" = str(user.id), convert back to int
        job_description=job_description,
        result=json.dumps(result)           # dict -> JSON string for SQLite TEXT column
    ))
    db.commit()
    return result\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What is Depends() in FastAPI and how does it work?',
       'Dependency injection. FastAPI resolves Depends() before calling the route function. '
       'Depends(get_current_user) calls get_current_user() first, injects its return value. '
       'If get_current_user raises HTTPException (invalid/expired token), '
       'FastAPI returns 401 and the route function never executes.')
    QA(s, st, 'Why is result stored as json.dumps() in the database?',
       'The analyses.result column is SQLAlchemy Text type — stores strings only. '
       'A Python dict cannot go into a text column directly. '
       'json.dumps() serializes to a JSON string. routes_history.py uses json.loads() to restore it. '
       'Tradeoff: cannot query individual fields (e.g. ats_score > 80) without parsing JSON in SQL.')
    QA(s, st, 'Why async def for the route when run_full_analysis is regular def?',
       'async def is needed to receive UploadFile (file uploads use async I/O). '
       'run_full_analysis is synchronous — all steps are CPU-bound Python, no async I/O '
       'except the Groq call (which langchain runs synchronously). '
       'FastAPI runs sync dependencies in a thread pool to avoid blocking the event loop.')
    s.append(PageBreak())

    # ── FILE 12 ───────────────────────────────────────────────────────────────
    H1(s, st, 'File 12 of 12  —  app/api/routes_compare.py')
    T(s, st, 'FIXED. Bug 1: score_sections() tuple stored without unpacking — caused blank page. '
             'Bug 2: ATS difference showed 12.400000000000006 — fixed with round(..., 2). '
             'Auth (Depends(get_current_user)) was also missing — now added. '
             'Does NOT use the full pipeline — comparison only needs skills + sections + ATS.')
    H2(s, st, 'The Bug That Caused a Blank Page')
    Code(s, """\
# BUG (old code):
section_scores_1 = score_sections(resume1_text)
# score_sections() returns TUPLE (scores_dict, feedback_dict)
# section_scores_1 held the WHOLE TUPLE
# calculate_ats_score called section_scores_1.get("Projects") -> AttributeError on tuple
# FastAPI serialized tuple as JSON array: [{...}, {...}]
# Frontend SectionScoreCard: Object.entries(array) -> returned indices ["0","1"]
# Tried to render {score}% where score was a whole dict object
# React: "Objects are not valid as a React child" -> component crash -> BLANK PAGE

# FIX:
section_scores_1, _ = score_sections(resume1_text)
# _ discards feedback_dict (not needed in compare route)
# section_scores_1 is now correctly the scores dict: {"Education": 70, "Projects": 85, ...}\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What does _ mean in tuple unpacking?',
       '_ is a valid Python variable name. Convention: means "I received this but discard it." '
       'a, _ = func() unpacks a two-element tuple — first element goes to a, '
       'second is stored in _ and never used. Seen everywhere: for i, _ in enumerate(items).')
    QA(s, st, 'Why two separate bugs from one wrong line?',
       'The missing unpack caused two independent failures. (1) Runtime: tuple has no .get() '
       '-> AttributeError -> 500. (2) Response: FastAPI serialized tuple as JSON array. '
       'Frontend received array, called Object.entries() -> got indices not section names '
       '-> tried to render a dict as text -> React crash -> blank page. Same root cause, '
       'two completely different failure modes.')
    QA(s, st, 'Why does the compare route not save to the database?',
       'The History page shows individual resume analyses. Comparisons involve two resumes — '
       'which do you save? Design decision: comparisons are one-time results. '
       'Saving them would need a different schema (two resume_id FK columns or separate table). '
       'Keeping it out avoids complexity.')

    H1(s, st, 'Bonus  —  app/main.py  —  Application Entry Point')
    T(s, st, 'Creates the FastAPI app object, runs database table creation at startup, '
             'adds CORS middleware, and registers all four routers. '
             'First file executed when you run: uvicorn app.main:app')
    H2(s, st, 'Key Code')
    Code(s, """\
from app.api.routes_resume  import router as resume_router   # "as" avoids name collision
from app.api.routes_compare import router as compare_router
from app.api.routes_auth    import router as auth_router
from app.api.routes_history import router as history_router

db_models.Base.metadata.create_all(bind=engine)   # CREATE TABLE if not exists — runs at startup

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],       # production: restrict to specific domain
    allow_credentials=True,    # allows Authorization header
    allow_methods=["*"],
    allow_headers=["*"],
)

# Merge all routers into the app — each adds its routes with its prefix
app.include_router(auth_router)     # POST /auth/register, POST /auth/login
app.include_router(resume_router)   # POST /resume/analyze
app.include_router(compare_router)  # POST /resume/compare
app.include_router(history_router)  # GET  /history

@app.api_route("/", methods=["GET", "HEAD"])   # HEAD for health-check monitors
def home():
    return {"message": "AI Resume Analyzer Running"}\
""")
    H2(s, st, 'Interview Q&A')
    QA(s, st, 'What is CORS and why is CORSMiddleware needed?',
       'Same-Origin Policy: browsers block requests from one origin (localhost:5173) to '
       'another (localhost:8000). CORS is the opt-in protocol. Browser sends preflight '
       'OPTIONS request first; server must reply with Access-Control-Allow-Origin header. '
       'CORSMiddleware adds these headers automatically. Without it, every axios call from '
       'React is blocked by the browser before it reaches the server.')
    QA(s, st, 'Why "as" when importing routers?',
       'All four route files export a variable named "router". Without aliasing, each import '
       'overwrites the previous — you\'d only have the last router. '
       '"from routes_resume import router as resume_router" renames each so all four coexist.')
    QA(s, st, 'What does create_all do and when is it not enough?',
       'create_all compares SQLAlchemy model metadata vs actual DB and runs CREATE TABLE for '
       'missing tables. Safe for first run. NOT for adding columns to existing tables — '
       'it ignores existing tables entirely. Production uses Alembic migrations which '
       'track and apply incremental schema changes (ALTER TABLE etc).')
    return s


# ══════════════════════════════════════════════════════════════════════════════
#  QUICK REVISION GUIDE
# ══════════════════════════════════════════════════════════════════════════════

def build_revision(st):
    s = []

    # Cover
    s.append(Spacer(1, 5 * cm))
    s.append(Paragraph('AI Resume Analyser', st['cover_title']))
    s.append(Paragraph('Interview Quick Revision Guide', st['cover_sub']))
    s.append(Spacer(1, 0.8 * cm))
    s.append(Paragraph('All key concepts, patterns, and interview Q&As in one place', st['note']))
    s.append(PageBreak())

    # ── Project snapshot ──────────────────────────────────────────────────────
    H1(s, st, 'Project at a Glance')
    Code(s, """\
Stack:   FastAPI (Python 3.10) + React (JS) + SQLite + Groq LLM (llama-3.1-8b)
Auth:    JWT (python-jose) — 24hr tokens stored in browser localStorage
PDF:     pdfplumber extracts text from uploaded PDFs
Pipeline: 11-step analysis — all steps share one ResumeAnalysisContext dataclass

ROUTES (all need Bearer token except /auth/*):
  POST /auth/register        create user, return JWT
  POST /auth/login           verify password, return JWT
  POST /resume/analyze       11-step pipeline + save to DB + return 16-field result
  POST /resume/compare       skill match + section score + ATS for 2 resumes (no DB save)
  GET  /history              user's past analyses from DB

PIPELINE STEP ORDER (cannot be changed without breaking dependencies):
  1 Name strip    3 Sections*   5 ATS*     7 Verdict     9 Recommendations
  2 Skills        4 Audit*      6 Recruiter  8 Priorities  10 Facts -> 11 LLM
  * Step 3 must precede 5. Step 4 must precede 6.\
""")
    s.append(PageBreak())

    # ── Python concepts ───────────────────────────────────────────────────────
    H1(s, st, 'Key Python Concepts Used')

    H2(s, st, '1. @dataclass + field(default_factory)')
    Code(s, """\
from dataclasses import dataclass, field

@dataclass
class MyClass:
    name: str                                    # required (no default)
    items: list = field(default_factory=list)    # CORRECT mutable default
    score: float = 0.0                           # immutable default — fine

# WRONG:  items: list = []   <- all instances share one list -> Python bug\
""")
    T(s, st, 'Why: default values are evaluated ONCE at class definition. = [] shares one list '
             'across all instances. default_factory calls list() fresh per instance.')

    H2(s, st, '2. Regex Patterns Used')
    Code(s, """\
# Name detection: 2-4 all-letter words
re.match(r'^[A-Za-z]+(?: [A-Za-z]+){1,3}$', line)

# Word boundary without \\b (handles node.js, ci/cd correctly)
re.search(r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])', text)

# Count occurrences in JD
re.findall(r'\\b' + re.escape(skill) + r'\\b', jd_lower)

# Emphasis word + skill within 40 chars
re.search('required' + r'.{0,40}' + 'python', jd_lower)

# GPA detection
re.search(r'(cgpa|gpa)\\s*[:\\-]?\\s*[\\d.]+', text)

# GitHub link
re.search(r'github\\.com/\\S+', text)

# Metrics (30%, 10x, 5000 users)
re.findall(r'\\d+\\s*[%x]|\\d[\\d,]+\\s*(users|requests|ms)', text)\
""")

    H2(s, st, '3. Tuple Unpacking with _')
    Code(s, """\
# Two-value tuple return — unpack both
cleaned_text, candidate_name = extract_and_strip_name(resume_text)
section_scores, section_feedback = score_sections(resume_text)

# Discard second value with _
section_scores_1, _ = score_sections(resume1_text)

# THE BUG: storing tuple without unpacking
section_scores = score_sections(text)      # WRONG — tuple not dict
section_scores.get("Projects")             # AttributeError: tuple has no .get()\
""")

    H2(s, st, '4. Set vs List for Membership Testing')
    Code(s, """\
# Set — O(1) hash lookup. Use when order/duplicates don't matter
CORE_SKILLS = {"python", "java", "react"}       # set literal
found_names  = {item["name"] for item in list}  # set comprehension

# List — O(n) scan. Use when order or duplicates matter
matched_skills = []

# In practice: "python" in set is instant; "python" in list scans every element\
""")

    H2(s, st, '5. Dispatch Dictionary Pattern')
    Code(s, """\
# Map keys to functions — eliminates if/elif chains
_SCORERS = {
    "Education": _score_education,
    "Projects":  _score_projects,
    "Skills":    _score_skills,
}

for section, scorer in _SCORERS.items():
    scores[section] = scorer(resume_text)    # calls the right function automatically

# Adding new section = one function + one dict entry. Zero changes to the loop.\
""")

    H2(s, st, '6. all() with Generator Expression')
    Code(s, """\
required = ["candidate_overview", "strengths", "improvement_areas", "recommended_actions"]

# Checks every key name exists — short-circuits on first missing key
if all(k in parsed for k in required):
    return parsed

# vs len(parsed) == 4  <- only checks count, not specific key names\
""")

    H2(s, st, '7. Safe Dict Reads with .get() Defaults')
    Code(s, """\
# Never raises KeyError — use default when key may be absent
resume_audit.get("found", [])            # empty list if "found" missing
section_scores.get("Experience", 100)    # 100 (not 0!) so "< 40" check fails safely
section_scores.get("Projects", 0)        # 0 so formula gives no credit if missing\
""")
    s.append(PageBreak())

    # ── FastAPI concepts ──────────────────────────────────────────────────────
    H1(s, st, 'Key FastAPI Concepts')

    H2(s, st, '1. APIRouter + include_router')
    Code(s, """\
# In each route file:
router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])
@router.post("/analyze")    # full path: POST /resume/analyze

# In main.py:
from app.api.routes_resume import router as resume_router  # "as" prevents name collision
app.include_router(resume_router)   # merges all routes into the main app\
""")

    H2(s, st, '2. Dependency Injection with Depends()')
    Code(s, """\
async def analyze_resume(
    resume: UploadFile = File(...),           # binary file, multipart form
    job_description: str = Form(...),          # text field, same multipart form
    current_user: dict = Depends(get_current_user),  # JWT validated BEFORE route runs
    db: Session = Depends(get_db)             # DB session opened, closed after route
):
# If get_current_user raises HTTPException -> route never executes -> 401 returned\
""")

    H2(s, st, '3. File() vs Form() vs Body()')
    B(s, st, 'File(...): reads binary file from multipart/form-data, wraps in UploadFile '
             'with .file, .filename, .content_type')
    B(s, st, 'Form(...): reads plain text field from multipart/form-data body')
    B(s, st, 'Body() / Pydantic model: reads JSON body — CANNOT mix with File() '
             '(different Content-Type headers)')
    B(s, st, 'File() and Form() CAN coexist in the same endpoint — both come from '
             'multipart/form-data')

    H2(s, st, '4. CORSMiddleware')
    Code(s, """\
# Same-Origin Policy blocks requests from localhost:5173 to localhost:8000 (diff ports)
# CORSMiddleware adds Access-Control-Allow-Origin header to every response

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],       # production: use ["https://yourdomain.com"]
    allow_credentials=True,    # allows Authorization header to pass through
    allow_methods=["*"],
    allow_headers=["*"],
)\
""")

    H2(s, st, '5. JWT Token Flow')
    Code(s, """\
# Login/Register:
token = create_access_token({"sub": str(user.id), "email": user.email})
# Token expires in 24 hours (ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24)

# Protected route:
# Header: Authorization: Bearer eyJhbG...
# get_current_user() decodes token -> {"sub": "1", "email": "..."}
# int(current_user["sub"]) -> user_id as integer for DB queries\
""")
    s.append(PageBreak())

    # ── File reference table ──────────────────────────────────────────────────
    H1(s, st, 'File-by-File Quick Reference')

    files = [
        ('analysis_context.py', 'NEW. Shared @dataclass with 17 fields flowing through all pipeline steps. '
                                'field(default_factory) for mutable defaults. Candidate name stored but never '
                                'sent to LLM.'),
        ('resume_parser.py', 'UPDATED. extract_resume_text() uses pdfplumber on file.file. '
                             'NEW extract_and_strip_name() regex-detects name in first 5 lines, '
                             'replaces with "the candidate". Returns tuple (cleaned, name).'),
        ('skill_matcher.py', 'REWRITTEN. NORMALIZATIONS dict (alias->canonical). SKILL_GROUPS for synonyms. '
                             'skill_in_text() uses negative lookbehind/lookahead regex. '
                             'seen set prevents double-counting. match_skills() returns (matched, missing).'),
        ('ats_score.py', 'REWRITTEN. 3 functions: calculate_ats_score() weighted 40/20/15/10/10/5%, '
                         'calculate_recruiter_fit_score() 6 factors, '
                         'compute_interview_probability() combined label (ATS x0.4 + recruiter x0.6).'),
        ('resume_verdict.py', 'REWRITTEN. Takes both ats_score + recruiter_fit_score. '
                              'Verdict label from ATS thresholds (>=80 Strong, >=60 Good, >=40 Average). '
                              'Imports compute_interview_probability from ats_score.py.'),
        ('section_scorer.py', 'REWRITTEN. Quality rubrics per section. Dispatch dict _SCORERS. '
                              '_feedback_level: >=70 high, >=40 medium, <40 low. '
                              'Returns TUPLE (scores_dict, feedback_dict) — must unpack with a, b = ...'),
        ('skill_priority.py', 'REWRITTEN. Scores each missing skill: JD frequency (max 30pts) + '
                              'emphasis word proximity (25pts) + category (Core 25/Preferred 15/Other 5). '
                              'Labels: Critical>=55, Important>=30, Nice to Have<30. Sorted.'),
        ('resume_checklist.py', 'UPDATED. generate_resume_checklist() audits 11 items (unchanged). '
                                'NEW generate_recommendations() reads audit+scores+priorities -> '
                                'up to 5 specific actions. Defaults to 100 not 0 for missing section keys.'),
        ('ai_analyzer.py', 'REWRITTEN. SYSTEM_PROMPT forbids name use + hallucination. '
                           'generate_ai_feedback_from_facts() sends structured facts only (no raw text, no name). '
                           '3-level fallback: JSON parse -> text parse -> rule-based.'),
        ('analysis_pipeline.py', 'NEW. Orchestrator. 11 steps. Steps 3+4 MUST precede 5+6. '
                                 '_build_structured_facts() creates name-free LLM input. '
                                 'LLM call last — only network call. run_full_analysis() is public entry point.'),
        ('routes_resume.py', 'UPDATED. Two service calls only: extract_resume_text + run_full_analysis. '
                             'Depends() for auth + DB. Saves result as json.dumps() to DB. '
                             'Flattens ctx.ai_feedback into top-level response fields.'),
        ('routes_compare.py', 'FIXED. Bug: score_sections() tuple unpacking missing -> blank page. '
                              'Fix: section_scores_1, _ = score_sections(). '
                              'Added Depends(get_current_user). No DB save. No full pipeline.'),
        ('main.py', 'create_all at startup. CORSMiddleware for cross-origin. '
                    '"as" aliases prevent router name collision. '
                    'include_router x4. HEAD method for health-check monitors.'),
    ]

    for filename, summary in files:
        H3(s, st, filename)
        T(s, st, summary)
        HR(s)

    s.append(PageBreak())

    # ── All interview Q&As ────────────────────────────────────────────────────
    H1(s, st, 'All Interview Q&As — Master List')

    qas = [
        ('Why use field(default_factory=list) instead of = []?',
         'Default values are evaluated ONCE at class definition. = [] shares ONE list across all instances — '
         'appending to one appends to all. default_factory=list calls list() fresh per new instance.'),
        ('What does @dataclass auto-generate?',
         '__init__ with all field parameters, __repr__ for printing, __eq__ for equality comparison. '
         'Eliminates ~50 lines of boilerplate for a 17-field class.'),
        ('Why use negative lookbehind/lookahead instead of \\b word boundaries?',
         '\\b considers "." non-word, so node.js breaks at the dot. Negative lookbehind (?<![a-z0-9]) '
         'and lookahead (?![a-z0-9]) check surrounding chars are not letters/digits, treating '
         'node.js as one token and preventing ml matching inside html.'),
        ('What does re.escape() do and why is it necessary?',
         're.escape() adds backslashes before special regex chars (. + * ? etc). '
         'Skills like node.js or c++ contain regex-special chars — without escape, '
         '"." in node.js means "any character", causing false positives.'),
        ('set vs list for membership testing — what is the difference?',
         '"x in set" is O(1) hash lookup. "x in list" is O(n) sequential scan. '
         'Use set for membership-only checks (no order/duplicates needed). '
         'Use list when order, index access, or duplicates matter.'),
        ('What is the dispatch dictionary pattern?',
         'Map keys to functions. Loop calls each function without knowing its name. '
         'Adding functionality = add function + one dict entry. No if/elif to modify. '
         'Used in section_scorer.py _SCORERS, keeps the main loop unchanged as features grow.'),
        ('Why must Step 3 (section scoring) run before Step 5 (ATS)?',
         'calculate_ats_score() uses section_scores in the weighted formula (20% projects, 15% exp...). '
         'If Step 5 ran before Step 3, section_scores is empty dict, formula silently gives '
         '0% for all sections — wrong result, no error, no warning.'),
        ('Why is the LLM call last in the pipeline (Step 11)?',
         'It needs facts from all previous steps. Also: if LLM fails, all deterministic scores '
         'are already computed and returned. Running LLM first means API failure loses everything.'),
        ('What caused the blank Compare Resume page?',
         'score_sections() returns tuple (scores_dict, feedback_dict). Old code stored the whole '
         'tuple as section_scores. FastAPI serialized it as JSON array. Frontend received array '
         'where SectionScoreCard expected dict. Object.entries(array) returned indices ["0","1"]. '
         'Rendering a dict object as {score}% caused React to throw "Objects are not valid as '
         'React child" — component crash — blank page. Fix: section_scores, _ = score_sections().'),
        ('What does _ mean in tuple unpacking?',
         '_ is a valid variable name. Convention: "I received this value but intentionally discard it." '
         'section_scores, _ = func() unpacks tuple — first to section_scores, second to _ (unused).'),
        ('What is Depends() in FastAPI?',
         'Dependency injection. FastAPI resolves Depends() before the route function runs. '
         'Depends(get_current_user) calls get_current_user() first; if it raises HTTPException, '
         'route never executes. Keeps auth logic out of route handlers.'),
        ('What is the difference between File() and Form() in FastAPI?',
         'Both come from multipart/form-data. File() expects binary data, wraps in UploadFile. '
         'Form() reads a plain text field. They CAN coexist. '
         'JSON body (Pydantic model) CANNOT mix with File() — different Content-Type.'),
        ('What is CORS and why is CORSMiddleware needed?',
         'Same-Origin Policy blocks browser requests between different origins (ports). '
         'CORS is the opt-in protocol — server adds Access-Control-Allow-Origin header. '
         'CORSMiddleware adds these automatically. Without it, all axios requests from React '
         'are blocked by the browser before reaching the server.'),
        ('Why "as" when importing routers in main.py?',
         'All four route files export a variable named "router". Without aliases, each import '
         'overwrites the previous. "from routes_resume import router as resume_router" '
         'renames each so all four coexist in memory simultaneously.'),
        ('Why store result as json.dumps() in SQLite?',
         'SQLAlchemy Text column stores strings only. json.dumps() serializes dict to JSON string. '
         'json.loads() restores it in the history route. Tradeoff: cannot query individual '
         'fields (ats_score > 80) without parsing JSON in the SQL query.'),
        ('What does create_all do and when is it not enough?',
         'create_all compares SQLAlchemy metadata vs DB — runs CREATE TABLE for missing tables. '
         'Safe for first run. NOT for schema changes to existing tables — it ignores them. '
         'Production uses Alembic migrations for incremental ALTER TABLE operations.'),
        ('Why strip the candidate name before the LLM?',
         'LLMs can inadvertently reveal PII or produce biased feedback when they know names. '
         'Replacing name with "the candidate" ensures privacy and forces objective analysis. '
         'SYSTEM_PROMPT also forbids name usage — but it can only forbid what was never given.'),
        ('Describe the three-level fallback chain in ai_analyzer.py.',
         'Level 1: LLM returns valid JSON — parse and validate all four required keys. '
         'Level 2: LLM returns plain text — _parse_text_response() extracts bullet sections. '
         'Level 3: LLM API throws exception — generate_fallback_from_facts() produces rule-based output. '
         'The endpoint never crashes regardless of LLM availability.'),
        ('Why does section_scores.get("Experience", 100) default to 100 not 0?',
         'If the key is missing, assume section is fine — do NOT trigger the recommendation. '
         'Defaulting to 0 would falsely add the action verb recommendation for every resume '
         'where Experience scoring is absent — a false positive.'),
        ('Why is llm = ChatGroq(...) at module level?',
         'Creating the client inside the function re-initializes HTTP connection on every call. '
         'At module level it is created once at import time and reused across all requests. '
         'For a function called on every resume upload, per-call initialization adds '
         'significant overhead.'),
        ('Why does interview probability weight recruiter_fit 60% vs ats_score 40%?',
         'ATS filters automatically via keyword matching. Actual hiring is human judgment. '
         'A candidate with strong soft signals (GitHub, metrics, action verbs) who slightly '
         'misses keyword matching is still a strong hire. Higher weight for recruiter fit '
         'reflects that human judgment matters more than automated keyword counts.'),
        ('Why is async def used for route handlers in FastAPI?',
         'UploadFile uses async I/O for file reading. Route functions receiving UploadFile '
         'must be async to handle the file stream. FastAPI runs sync functions in a thread '
         'pool — fine for CPU-bound work but cannot handle async file reading.'),
        ('What is @app.api_route vs @app.get?',
         '@app.get registers only GET. @app.api_route(methods=["GET","HEAD"]) registers both. '
         'HEAD is needed for health-check monitors — they check server is alive without '
         'downloading the body. Without HEAD support, monitors report the server as down.'),
    ]

    for q, a in qas:
        QA(s, st, q, a)
    s.append(PageBreak())

    # ── Patterns cheat sheet ──────────────────────────────────────────────────
    H1(s, st, 'Key Patterns Cheat Sheet')

    patterns = [
        ('Centralized Pipeline Pattern',
         'One dataclass flows through all steps. Each step reads from it and writes back. '
         'No function holds its own copy of raw text. No re-computation. '
         'New step = new function + one line in run_full_analysis().'),
        ('Dispatch Dictionary Pattern',
         'Map keys to functions. Loop calls each. Adding features = add function + add dict entry. '
         'Loop code never changes. Open/closed principle in practice.'),
        ('Three-Level Fallback Chain',
         'LLM JSON parse -> text parse -> rule-based fallback. '
         'Each level catches what the level above misses. Endpoint always returns valid shape.'),
        ('Dependency Injection (FastAPI Depends)',
         'Depends() resolves auth and DB session before route runs. '
         'Route functions receive already-validated dependencies. '
         'Auth and DB lifecycle completely separated from business logic.'),
        ('Private Functions with _ Prefix',
         'Leading _ marks functions as internal. Not enforced — convention only. '
         'Signals "do not import from outside this module." '
         'Used for _build_structured_facts, _score_education, _feedback_level.'),
        ('Module-Level Client Initialization',
         'llm = ChatGroq(...) at module level. Created once at import. Reused across all requests. '
         'Standard pattern for any heavy client: database connections, API clients, ML models.'),
        ('Safe Dict Reads with .get() and Smart Defaults',
         'dict.get("key", default) never raises KeyError. '
         'Choose default based on what behaviour you want when key is absent — '
         'not just 0 or []. Use 100 when absence should NOT trigger a condition.'),
        ('Tuple Unpacking with _',
         'a, _ = func() unpacks and discards second value. '
         'Convention communicates intentional discard. '
         'The bug in compare route was the ABSENCE of this unpacking.'),
    ]

    for name, desc in patterns:
        H3(s, st, name)
        T(s, st, desc)
        HR(s)

    return s


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    styles = make_styles()

    print("Generating detailed study guide...")
    doc1 = SimpleDocTemplate(
        'AI_Resume_Analyser_Study_Guide.pdf',
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    doc1.build(build_detailed(styles))
    print("  -> AI_Resume_Analyser_Study_Guide.pdf")

    print("Generating quick revision guide...")
    doc2 = SimpleDocTemplate(
        'AI_Resume_Analyser_Quick_Revision.pdf',
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    doc2.build(build_revision(styles))
    print("  -> AI_Resume_Analyser_Quick_Revision.pdf")

    print("\nDone. Both PDFs saved in project root.")


if __name__ == '__main__':
    main()
