import os
import re

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resume_path = os.path.join(BASE_DIR, "data", "resume.txt")
job_path = os.path.join(BASE_DIR, "data", "job_description.txt")

# ---------------- UTILITY FUNCTIONS ----------------
def load_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if not text:
                print(f"⚠️ Warning: {file_path} is empty.")
            return text
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found.")
        return ""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize(text):
    return text.split()

STOPWORDS = {
    "the", "is", "and", "with", "for", "a", "an",
    "to", "of", "in", "on", "at", "by", "from"
}

def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOPWORDS]

def preprocess_text(text):
    if not text:
        return []

    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    return remove_stopwords(tokens)

# ---------------- SKILL LOGIC ----------------
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
    "natural language processing": {"nlp"}
}

def normalize_skill(skill):
    for main_skill, aliases in SKILL_ALIASES.items():
        if skill == main_skill or skill in aliases:
            return main_skill
    return skill

def extract_skills(tokens, skill_set):
    found_skills = set()

    for word in tokens:
        normalized = normalize_skill(word)
        if normalized in skill_set:
            found_skills.add(normalized)

    for i in range(len(tokens) - 1):
        two_word = tokens[i] + " " + tokens[i + 1]
        normalized = normalize_skill(two_word)
        if normalized in skill_set:
            found_skills.add(normalized)

    return found_skills

def match_skills(resume_skills, job_skills):
    if not job_skills:
        return 0, set(), set()

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    score = int((len(matched) / len(job_skills)) * 100)
    return score, matched, missing

# ---------------- MAIN EXECUTION ----------------
def main():
    resume_text = load_text(resume_path)
    job_text = load_text(job_path)

    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

    resume_skills = extract_skills(resume_tokens, SKILLS)
    job_skills = extract_skills(job_tokens, SKILLS)

    match_score, matched_skills, missing_skills = match_skills(
        resume_skills, job_skills
    )

    print("\n===== FINAL RESULT =====")
    print(f"Match Score: {match_score}%")

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

