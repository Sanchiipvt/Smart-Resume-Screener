# Smart-Resume-Screener
# Smart Resume Screener (ATS Simulator)

An ATS-style resume screening system that evaluates resumes against job descriptions using a hybrid of:
- Rule-based skill matching
- ML-based semantic similarity (TF-IDF + cosine similarity)

## Features
- PDF & DOCX resume parsing
- Job description comparison
- Skill extraction with aliases
- Skill match percentage
- TF-IDF similarity score
- Final ATS compatibility score
- Resume improvement suggestions
- Recruiter-style verdict

## Tech Stack
- Python
- Streamlit
- scikit-learn
- pdfplumber
- python-docx

## How It Works
1. Resume and job description are converted to text
2. Text is cleaned and tokenized
3. Skills are extracted and matched
4. Semantic similarity is computed using TF-IDF
5. A weighted ATS score is generated

## Why This Project?
Most resume screeners are black boxes.  
This project focuses on **interpretability**, showing *why* a resume is accepted or rejected.

## Future Improvements
- ML-based skill extraction (NER)
- Section-wise ATS scoring
- Resume keyword optimization

##Section	How it should be scored
- Skills	       Rule-based skill matching
- Experience	   TF-IDF similarity
- Projects	     TF-IDF similarity
- Education    	 Keyword presence (light TF-IDF)
