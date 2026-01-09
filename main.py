# =========================
# IMPORTS
# =========================
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
from docx import Document


# =========================
# FILE TEXT EXTRACTION
# =========================
def extract_text_from_file(uploaded_file):
    """
    Extract text from PDF or DOCX file.
    """
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text.strip()

    elif file_name.endswith(".docx"):
        doc = Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])

    return ""


# =========================
# TEXT PREPROCESSING
# =========================
STOPWORDS = {
    "the", "is", "and", "with", "for", "a", "an",
    "to", "of", "in", "on", "at", "by", "from"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_text(text):
    if not text:
        return []
    tokens = clean_text(text).split()
    return [t for t in tokens if t not in STOPWORDS]


# =========================
# SKILLS & SUGGESTIONS
# =========================
SKILLS = {
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "data visualization",
    "nlp",
    "tensorflow",
    "pandas",
    "numpy"
}

SKILL_ALIASES = {
    "machine learning": {"ml", "machine-learning"},
    "deep learning": {"dl", "deep-learning"},
    "data analysis": {"data-analysis", "analytics"},
    "python": {"py"},
    "nlp": {"natural language processing"}
}

SKILL_SUGGESTIONS = {
    "python": "Add Python projects demonstrating data handling or automation.",
    "java": "Include object-oriented or backend development projects.",
    "sql": "Show experience with joins, subqueries, and database design.",
    "machine learning": "Add ML projects with model training and evaluation.",
    "deep learning": "Include neural network or deep learning implementations.",
    "data analysis": "Show data cleaning, analysis, and insight generation.",
    "data visualization": "Add dashboards or charts using Matplotlib or Seaborn.",
    "nlp": "Mention NLP tasks like text classification or sentiment analysis.",
    "tensorflow": "Include hands-on TensorFlow model implementations.",
    "pandas": "Show data manipulation using Pandas.",
    "numpy": "Mention numerical computing or matrix-based work."
}


# =========================
# SKILL LOGIC
# =========================
def normalize_skill(skill):
    for main_skill, aliases in SKILL_ALIASES.items():
        if skill == main_skill or skill in aliases:
            return main_skill
    return skill

def extract_skills(tokens, skill_set):
    found = set()

    for word in tokens:
        norm = normalize_skill(word)
        if norm in skill_set:
            found.add(norm)

    for i in range(len(tokens) - 1):
        phrase = tokens[i] + " " + tokens[i + 1]
        norm = normalize_skill(phrase)
        if norm in skill_set:
            found.add(norm)

    return found

def match_skills(resume_skills, job_skills):
    if not job_skills:
        return 0, set(), set()

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    score = int((len(matched) / len(job_skills)) * 100)

    return score, matched, missing


# =========================
# ML SCORING
# =========================
def tfidf_similarity(resume_text, job_text):
    if not resume_text or not job_text:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([
        clean_text(resume_text),
        clean_text(job_text)
    ])

    return round(cosine_similarity(vectors[0], vectors[1])[0][0] * 100, 2)


# =========================
# FINAL SCORE
# =========================
def final_ats_score(skill_score, tfidf_score, skill_weight=0.7):
    return round(
        skill_score * skill_weight + tfidf_score * (1 - skill_weight),
        2
    )


# =========================
# SUGGESTION ENGINE
# =========================
def generate_skill_suggestions(missing_skills):
    return [
        SKILL_SUGGESTIONS.get(
            skill,
            f"Consider adding experience related to {skill}."
        )
        for skill in missing_skills
    ]
