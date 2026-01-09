import streamlit as st
from main import (
    extract_text_from_file,
    preprocess_text,
    extract_skills,
    match_skills,
    tfidf_similarity,
    final_ats_score,
    generate_skill_suggestions,
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
uploaded_jd = st.file_uploader(
    "Upload Job Description (PDF or DOCX)",
    type=["pdf", "docx"]
)

job_text_input = st.text_area(
    "Or paste Job Description text",
    height=200
)

# ---------------- BUTTON ACTION ----------------
if st.button("🔍 Screen Resume"):

    if not uploaded_resume:
        st.warning("Please upload a resume.")
        st.stop()

    # Decide JD source
    if uploaded_jd:
        job_text = extract_text_from_file(uploaded_jd)
    else:
        job_text = job_text_input

    if not job_text.strip():
        st.warning("Please upload or paste a job description.")
        st.stop()

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
    st.write(", ".join(sorted(matched)) if matched else "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(sorted(missing)) if missing else "None")

    # ---------------- SUGGESTIONS ----------------
    st.subheader("💡 Suggested Improvements")
    suggestions = generate_skill_suggestions(missing)

    if suggestions:
        for s in suggestions:
            st.write(f"• {s}")
    else:
        st.write("Your resume already matches the job requirements well.")


