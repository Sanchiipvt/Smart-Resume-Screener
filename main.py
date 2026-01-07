import os
import re

# Get base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths safely
resume_path = os.path.join(BASE_DIR, "data", "resume.txt")
job_path = os.path.join(BASE_DIR, "data", "job_description.txt")

def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
resume_text = load_text(resume_path)
job_text = load_text(job_path)

with open(job_path, "r", encoding="utf-8") as f:
    job_text = f.read()
    
def clean_text(text):
    text = text.lower()                 # lowercase
    text = re.sub(r'[^a-z\s]', '', text) # remove punctuation & numbers
    text = re.sub(r'\s+', ' ', text)     # remove extra spaces
    return text.strip()

def preprocess_text(text):
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    filtered = remove_stopwords(tokens)
    return filtered

clean_resume = clean_text(resume_text)
clean_job = clean_text(job_text)

def tokenize(text):
    return text.split(" ")


STOPWORDS = {
    "the", "is", "and", "with", "for", "a", "an",
    "to", "of", "in", "on", "at", "by", "from"
}

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

def extract_skills(tokens, skill_set):
    found_skills = set()
    
    # single-word skills
    for word in tokens:
        if word in skill_set:
            found_skills.add(word)
    
    # two-word skills
    for i in range(len(tokens) - 1):
        two_word = tokens[i] + " " + tokens[i + 1]
        if two_word in skill_set:
            found_skills.add(two_word)
    
    return found_skills

def match_skills(resume_skills, job_skills):
    matched = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)
    
    if len(job_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(job_skills)) * 100
    
    return round(score, 2), matched, missing


def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOPWORDS]

filtered_resume = preprocess_text(resume_text)
filtered_job = preprocess_text(job_text)

resume_skills = extract_skills(filtered_resume, SKILLS)
job_skills = extract_skills(filtered_job, SKILLS)

match_score, matched_skills, missing_skills = match_skills(
    resume_skills, job_skills
)

def main():
    resume_text = load_text(resume_path)
    job_text = load_text(job_path)

    filtered_resume = preprocess_text(resume_text)
    filtered_job = preprocess_text(job_text)

    resume_skills = extract_skills(filtered_resume, SKILLS)
    job_skills = extract_skills(filtered_job, SKILLS)

    score, matched, missing = match_skills(resume_skills, job_skills)

    print("\n===== FINAL RESULT =====")
    print(f"Match Score: {score}%")
    print("Matched Skills:", matched)
    print("Missing Skills:", missing)

if __name__ == "__main__":
    main()
