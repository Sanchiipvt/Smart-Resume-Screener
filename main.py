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

print("===== CLEANED RESUME =====")
print(clean_resume)

print("\n===== CLEANED JOB DESCRIPTION =====")
print(clean_job)
