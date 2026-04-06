import streamlit as st
from fpdf import FPDF
import random

# --- Page Config ---
st.set_page_config(page_title="AI Study Generator", page_icon="🧠")

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- PDF ---
def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_path = "study_material.pdf"
    pdf.output(file_path)
    return file_path

# --- FAKE AI (works always) ---
def generate_ai_content(subject, topic, difficulty, format_type, num_questions):
    questions = []

    for i in range(1, num_questions + 1):
        if format_type == "MCQ":
            q = f"""
Q{i}. What is {topic} in {subject}?
A. Option 1  
B. Option 2  
C. Option 3  
D. Option 4  
Answer: A
"""
        elif format_type == "Flashcards":
            q = f"""
Front: Define {topic}
Back: {topic} is an important concept in {subject}.
"""
        elif format_type == "Short Answer":
            q = f"""
Q{i}. Explain {topic}.
Answer: {topic} is a key concept in {subject} explained briefly.
"""
        else:
            q = f"""
Q{i}. Discuss {topic} in detail.
Answer: Detailed explanation of {topic} in {subject}.
"""

        questions.append(q)

    return "\n".join(questions)

# --- UI ---
st.title("🧠 AI Study Generator (Offline Version)")
st.write("Works without API — always runs!")

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject")
    topic = st.text_input("Topic")
    difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])

with col2:
    q_format = st.selectbox("Format", ["MCQ", "Flashcards", "Short Answer", "Long Answer"])
    num_questions = st.slider("Number of Questions", 1, 5, 3)

# --- Generate ---
if st.button("🚀 Generate"):
    if subject and topic:
        result = generate_ai_content(subject, topic, difficulty, q_format, num_questions)
        st.session_state.current_result = result
        st.session_state.history.append(result)
    else:
        st.error("Enter subject and topic")

# --- Output ---
if "current_result" in st.session_state:
    st.subheader("📘 Output")
    st.text(st.session_state.current_result)

    st.download_button("Download Text", st.session_state.current_result)

    if st.button("Generate PDF"):
        pdf_file = create_pdf(st.session_state.current_result)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f)

# --- History ---
st.subheader("🕘 History")
for item in st.session_state.history[::-1]:
    st.write(item)