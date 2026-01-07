import os
import re

# Get base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths safely
resume_path = os.path.join(BASE_DIR, "data", "resume.txt")
job_path = os.path.join(BASE_DIR, "data", "job_description.txt")

# Read files
with open(resume_path, "r", encoding="utf-8") as f:
    resume_text = f.read()

with open(job_path, "r", encoding="utf-8") as f:
    job_text = f.read()
    
def clean_text(text):
    text = text.lower()                 # lowercase
    text = re.sub(r'[^a-z\s]', '', text) # remove punctuation & numbers
    text = re.sub(r'\s+', ' ', text)     # remove extra spaces
    return text.strip()

clean_resume = clean_text(resume_text)
clean_job = clean_text(job_text)

def tokenize(text):
    return text.split(" ")

resume_tokens = tokenize(clean_resume)
job_tokens = tokenize(clean_job)

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

filtered_resume = remove_stopwords(resume_tokens)
filtered_job = remove_stopwords(job_tokens)

resume_skills = extract_skills(filtered_resume, SKILLS)
job_skills = extract_skills(filtered_job, SKILLS)

match_score, matched_skills, missing_skills = match_skills(
    resume_skills, job_skills
)

print("===== CLEANED RESUME =====")
print(clean_resume)

print("\n===== CLEANED JOB DESCRIPTION =====")
print(clean_job)

print("\n===== TOKENIZED & CLEANED RESUME =====")
print(filtered_resume)

print("\n===== TOKENIZED & CLEANED JOB DESCRIPTION =====")
print(filtered_job)

print("\n===== RESUME SKILLS =====")
print(resume_skills)

print("\n===== JOB REQUIRED SKILLS =====")
print(job_skills)

print("\n===== MATCH RESULTS =====")
print(f"Match Score: {match_score}%")

print("\nMatched Skills:")
print(matched_skills)

print("\nMissing Skills:")
print(missing_skills)
