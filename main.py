# =========================
# IMPORTS
# =========================
import re
import pdfplumber
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# FILE TEXT EXTRACTION
# =========================
def extract_text_from_file(uploaded_file):
    """
    Extract text from PDF or DOCX file.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text.strip()

    elif filename.endswith(".docx"):
        doc = Document(uploaded_file)
        return " ".join(p.text for p in doc.paragraphs)

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
# SKILLS, ALIASES & SUGGESTIONS
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
    "data analysis": {"analytics", "data-analysis"},
    "python": {"py"},
    "nlp": {"natural language processing"}
}

SKILL_SUGGESTIONS = {
    "python": "Add Python projects demonstrating automation or data handling.",
    "java": "Include object-oriented or backend development projects.",
    "sql": "Show complex queries, joins, and database schema design.",
    "machine learning": "Add ML projects with model training and evaluation.",
    "deep learning": "Include neural networks or CNN/RNN implementations.",
    "data analysis": "Show data cleaning, EDA, and insights generation.",
    "data visualization": "Add dashboards using Matplotlib, Seaborn, or Power BI.",
    "nlp": "Mention NLP tasks like text classification or sentiment analysis.",
    "tensorflow": "Include hands-on TensorFlow model implementations.",
    "pandas": "Show real-world data manipulation pipelines.",
    "numpy": "Mention numerical computing or matrix-based operations."
}

# =========================
# SKILL MATCHING LOGIC
# =========================
def normalize_skill(skill):
    for main, aliases in SKILL_ALIASES.items():
        if skill == main or skill in aliases:
            return main
    return skill

def extract_skills(tokens, skill_set):
    found = set()

    # single-word
    for token in tokens:
        norm = normalize_skill(token)
        if norm in skill_set:
            found.add(norm)

    # two-word
    for i in range(len(tokens) - 1):
        phrase = normalize_skill(tokens[i] + " " + tokens[i + 1])
        if phrase in skill_set:
            found.add(phrase)

    return found

def match_skills(resume_skills, job_skills):
    if not job_skills:
        return 0, set(), set()

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    score = int((len(matched) / len(job_skills)) * 100)

    return score, matched, missing

def generate_skill_suggestions(missing_skills):
    return [
        SKILL_SUGGESTIONS.get(
            skill,
            f"Consider adding experience related to {skill}."
        )
        for skill in missing_skills
    ]

# =========================
# ML-BASED SIMILARITY
# =========================
def tfidf_similarity(resume_text, job_text):
    if not resume_text or not job_text:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform([
        clean_text(resume_text),
        clean_text(job_text)
    ])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(similarity * 100, 2)

# =========================
# FINAL ATS SCORE
# =========================
def final_ats_score(skill_score, tfidf_score, skill_weight=0.7):
    return round(
        (skill_score * skill_weight) +
        (tfidf_score * (1 - skill_weight)),
        2
    )
