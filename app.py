import streamlit as st
from main import (
    preprocess_text,
    extract_skills,
    match_skills,
    tfidf_similarity,
    final_ats_score,
    SKILLS
)

st.set_page_config(page_title="Smart Resume Screener", layout="centered")

st.title("📄 Smart Resume Screener")
st.write("ATS-style resume screening using rule-based + ML scoring")

# Input areas
resume_text = st.text_area("Paste Resume Text", height=200)
job_text = st.text_area("Paste Job Description", height=200)

if st.button("🔍 Screen Resume"):
    if not resume_text or not job_text:
        st.warning("Please provide both resume and job description.")
    else:
        # ML score
        tfidf_score = tfidf_similarity(resume_text, job_text)

        # Skill matching
        resume_tokens = preprocess_text(resume_text)
        job_tokens = preprocess_text(job_text)

        resume_skills = extract_skills(resume_tokens, SKILLS)
        job_skills = extract_skills(job_tokens, SKILLS)

        skill_score, matched, missing = match_skills(
            resume_skills, job_skills
        )

        final_score = final_ats_score(skill_score, tfidf_score)

        # Results
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
