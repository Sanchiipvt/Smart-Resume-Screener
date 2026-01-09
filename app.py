import streamlit as st
from main import (
    extract_text_from_file,
    preprocess_text,
    extract_skills,
    match_skills,
    tfidf_similarity,
    final_ats_score,
    SKILLS
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Resume Screener", layout="centered")

st.title("📄 Smart Resume Screener")
st.write("ATS-style resume screening using rule-based + ML scoring")

# ---------------- INPUTS ----------------
st.subheader("📄 Upload Resume")
uploaded_resume = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

st.subheader("🧾 Job Description")
job_text = st.text_area("Paste Job Description", height=200)

# ---------------- BUTTON ACTION ----------------
if st.button("🔍 Screen Resume"):

    # Validation
    if not uploaded_resume:
        st.warning("Please upload a resume.")
        st.stop()

    if not job_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    # Extract resume text
    resume_text = extract_text_from_file(uploaded_resume)

    if not resume_text.strip():
        st.warning("Unable to extract text from resume.")
        st.stop()

    # ---------------- SCORING ----------------
    tfidf_score = tfidf_similarity(resume_text, job_text)

    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

    resume_skills = extract_skills(resume_tokens, SKILLS)
    job_skills = extract_skills(job_tokens, SKILLS)

    skill_score, matched, missing = match_skills(
        resume_skills, job_skills
    )

    final_score = final_ats_score(skill_score, tfidf_score)

    # ---------------- RESULTS ----------------
    st.subheader("📊 Results")
    st.metric("Skill Match Score", f"{skill_score}%")
    st.metric("TF-IDF Similarity Score", f"{tfidf_score}%")
    st.metric("⭐ Final ATS Score", f"{final_score}%")

    st.subheader("✅ Matched Skills")
    if matched:
        st.write(", ".join(sorted(matched)))
    else:
        st.write("None")

    st.subheader("❌ Missing Skills")
    if missing:
        st.write(", ".join(sorted(missing)))
    else:
        st.write("None")
