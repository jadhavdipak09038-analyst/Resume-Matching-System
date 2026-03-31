import streamlit as st
import pickle
import docx
import PyPDF2

# -----------------------------
# Load Model & Vectorizer
# -----------------------------
model = pickle.load(open("models/role_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

# -----------------------------
# Extract text from PDF / DOCX
# -----------------------------
def extract_text(file):

    text = ""

    # PDF
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    # DOCX
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text.lower()


# -----------------------------
# Extract Skills
# -----------------------------
def extract_skills(text):

    skills_keywords = [
        "python","sql","excel","power bi","tableau",
        "html","css","javascript","react","node",
        "machine learning","data analysis"
    ]

    found = [skill for skill in skills_keywords if skill in text]

    return found


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("📄 Resume Matching System")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)", type=["pdf", "docx"]
)

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is not None:

    # Extract text
    text = extract_text(uploaded_file)

    # ❗ Handle empty text
    if text.strip() == "":
        st.error("Unable to extract text from resume!")
        st.stop()

    # Extract skills
    skills = extract_skills(text)

    # ❗ Handle no skills found
    if len(skills) == 0:
        st.warning("No relevant skills found in resume!")
        st.stop()

    st.subheader("🧠 Extracted Candidate Skills")
    st.write(", ".join(skills))

    # -----------------------------
    # Prepare input for model
    # -----------------------------
    combined_text = " ".join(skills)

    X = vectorizer.transform([combined_text])

    # -----------------------------
    # Prediction using probabilities
    # -----------------------------
    try:
        probs = model.predict_proba(X)[0]
    except:
        st.error("Model does not support probability prediction!")
        st.stop()

    roles = model.classes_

    role_scores = list(zip(roles, probs * 100))
    role_scores.sort(key=lambda x: x[1], reverse=True)

    top3 = role_scores[:3]

    # ✅ FINAL FIX (NO MISMATCH)
    best_role = top3[0][0]
    best_score = round(top3[0][1], 2)

    # -----------------------------
    # UI Output
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Candidate Fit Score")
        st.progress(int(best_score))
        st.write(f"### Overall Fit Score: {best_score}%")

        # Bonus label
        if best_score > 70:
            st.success("High Match ✅")
        elif best_score > 40:
            st.warning("Moderate Match ⚠️")
        else:
            st.error("Low Match ❌")

    with col2:
        st.subheader("🎯 Best Role")
        st.success(f"{best_role} ({best_score}%)")

    st.subheader("🏆 Top Role Recommendations")

    for role, score in top3:
        st.write(f"👉 {role} — {round(score,2)}%")