import streamlit as st
from main import (
    extract_text_from_file,
    preprocess_text,
    extract_skills,
    match_skills,
    generate_skill_suggestions,
    tfidf_similarity,
    final_ats_score,
    SKILLS
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Resume Screener",
    layout="centered"
)

st.title("📄 Smart Resume Screener")
st.write("ATS-style resume screening using rule-based + ML scoring")

# =========================
# INPUTS
# =========================
st.subheader("📄 Upload Resume")
uploaded_resume = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

st.subheader("🧾 Job Description")
job_text = st.text_area(
    "Paste Job Description",
    height=200
)

# =========================
# SCREEN BUTTON
# =========================
if st.button("🔍 Screen Resume"):

    if not uploaded_resume:
        st.warning("Please upload a resume.")
        st.stop()

    if not job_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    resume_text = extract_text_from_file(uploaded_resume)

    if not resume_text.strip():
        st.warning("Unable to extract text from resume.")
        st.stop()

    # =========================
    # SCORING PIPELINE
    # =========================
    tfidf_score = tfidf_similarity(resume_text, job_text)

    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

    resume_skills = extract_skills(resume_tokens, SKILLS)
    job_skills = extract_skills(job_tokens, SKILLS)

    skill_score, matched, missing = match_skills(
        resume_skills, job_skills
    )

    final_score = final_ats_score(skill_score, tfidf_score)
    
from main import split_resume_sections, section_wise_scores

sections = split_resume_sections(resume_text)
section_scores = section_wise_scores(sections, job_text)

st.subheader("📂 Section-wise ATS Breakdown")

for section, score in section_scores.items():
    st.write(f"**{section.capitalize()}**")
    st.progress(score / 100)
    st.write(f"{score}%")

    # =========================
    # RESULTS
    # =========================
    st.subheader("📊 ATS Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Skill Match", f"{skill_score}%")
    c2.metric("TF-IDF Match", f"{tfidf_score}%")
    c3.metric("⭐ Final ATS", f"{final_score}%")

    st.subheader("🧠 Skill Coverage")
    if job_skills:
        st.progress(len(matched) / len(job_skills))
        st.write(f"Matched: {len(matched)} / {len(job_skills)}")
        st.write(f"Missing: {len(missing)} / {len(job_skills)}")

    st.subheader("✅ Matched Skills")
    st.write(", ".join(sorted(matched)) if matched else "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(sorted(missing)) if missing else "None")

    # =========================
    # SUGGESTIONS
    # =========================
    st.subheader("💡 Resume Improvement Suggestions")
    suggestions = generate_skill_suggestions(missing)

    if suggestions:
        for s in suggestions:
            st.write("•", s)
    else:
        st.success("Your resume already aligns well with the job role.")

    # =========================
    # RECRUITER VERDICT
    # =========================
    st.subheader("📌 Recruiter Verdict")
    if final_score >= 85:
        st.success("🟢 Shortlist Immediately")
    elif final_score >= 70:
        st.warning("🟡 Consider After Review")
    else:
        st.error("🔴 Reject / Needs Rewrite")


