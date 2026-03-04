import streamlit as st
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Text Cleaning Function
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# Resume Matching Class
# -----------------------------
class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_match(self, resume_text, job_description):
        resume_text = clean_text(resume_text)
        job_description = clean_text(job_description)

        documents = [resume_text, job_description]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return round(similarity[0][0] * 100, 2)

    def classify_score(self, score):
        if score >= 75:
            return "🔥 Strong Match"
        elif score >= 50:
            return "👍 Moderate Match"
        else:
            return "❌ Weak Match"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("🤖 AI Resume Screening System")
st.write("Mini ATS using NLP & Machine Learning")

col1, col2 = st.columns(2)

with col1:
    resume_input = st.text_area("📄 Paste Resume Text", height=300)

with col2:
    job_input = st.text_area("💼 Paste Job Description", height=300)

if st.button("Analyze Match"):

    if resume_input and job_input:
        matcher = ResumeMatcher()
        score = matcher.calculate_match(resume_input, job_input)
        classification = matcher.classify_score(score)

        st.subheader("📊 Results")
        st.metric(label="Match Score", value=f"{score}%")
        st.success(f"Classification: {classification}")

        st.progress(int(score))

    else:
        st.warning("Please enter both Resume and Job Description.")

st.markdown("---")
st.markdown("Built with ❤️ using Python, Scikit-learn, and Streamlit")