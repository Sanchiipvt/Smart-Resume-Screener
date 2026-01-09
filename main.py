# =========================
# IMPORTS
# =========================
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# PATH CONFIGURATION
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUME_PATH = os.path.join(BASE_DIR, "data", "resume.txt")
JOB_PATH = os.path.join(BASE_DIR, "data", "job_description.txt")


# =========================
# FILE HANDLING
# =========================
def load_text(file_path):
    """
    Safely load text from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if not text:
                print(f"⚠️ Warning: {file_path} is empty.")
            return text
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found.")
        return ""


# =========================
# TEXT PREPROCESSING
# =========================
STOPWORDS = {
    "the", "is", "and", "with", "for", "a", "an",
    "to", "of", "in", "on", "at", "by", "from"
}

def clean_text(text):
    """
    Normalize text by lowercasing and removing punctuation.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def tokenize(text):
    return text.split()

def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOPWORDS]

def preprocess_text(text):
    """
    Full preprocessing pipeline.
    """
    if not text:
        return []
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    return remove_stopwords(tokens)


# =========================
# SKILL EXTRACTION LOGIC
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

def normalize_skill(skill):
    """
    Convert aliases to canonical skill names.
    """
    for main_skill, aliases in SKILL_ALIASES.items():
        if skill == main_skill or skill in aliases:
            return main_skill
    return skill

def extract_skills(tokens, skill_set):
    """
    Extract single-word and multi-word skills.
    """
    found_skills = set()

    # Single-word skills
    for word in tokens:
        normalized = normalize_skill(word)
        if normalized in skill_set:
            found_skills.add(normalized)

    # Two-word skills
    for i in range(len(tokens) - 1):
        phrase = tokens[i] + " " + tokens[i + 1]
        normalized = normalize_skill(phrase)
        if normalized in skill_set:
            found_skills.add(normalized)

    return found_skills

def match_skills(resume_skills, job_skills):
    """
    Compare resume skills against job skills.
    """
    if not job_skills:
        return 0, set(), set()

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    score = int((len(matched) / len(job_skills)) * 100)

    return score, matched, missing


# =========================
# ML-BASED SCORING
# =========================
def tfidf_similarity(resume_text, job_text):
    """
    Compute semantic similarity using TF-IDF + cosine similarity.
    """
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
# FINAL ATS SCORING
# =========================
def final_ats_score(skill_score, tfidf_score, skill_weight=0.7):
    """
    Weighted final ATS score.
    """
    tfidf_weight = 1 - skill_weight
    final_score = (skill_score * skill_weight) + (tfidf_score * tfidf_weight)
    return round(final_score, 2)


# =========================
# MAIN EXECUTION
# =========================
def main():
    resume_text = load_text(RESUME_PATH)
    job_text = load_text(JOB_PATH)

    # ML similarity score
    tfidf_score = tfidf_similarity(resume_text, job_text)

    # Rule-based skill matching
    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

    resume_skills = extract_skills(resume_tokens, SKILLS)
    job_skills = extract_skills(job_tokens, SKILLS)

    skill_score, matched_skills, missing_skills = match_skills(
        resume_skills, job_skills
    )

    # Final ATS score
    final_score = final_ats_score(skill_score, tfidf_score)

    # Output
    print("\n===== ATS SCREENING RESULT =====")
    print(f"Skill Match Score: {skill_score}%")
    print(f"TF-IDF Similarity Score: {tfidf_score}%")
    print(f"⭐ Final ATS Score: {final_score}%")

    print("\nMatched Skills:")
    if matched_skills:
        for skill in sorted(matched_skills):
            print(f"✔ {skill}")
    else:
        print("None")

    print("\nMissing Skills:")
    if missing_skills:
        for skill in sorted(missing_skills):
            print(f"✘ {skill}")
    else:
        print("None")


if __name__ == "__main__":
    main()
