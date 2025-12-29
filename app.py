import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI Career Advisor", layout="centered")
st.title("🎓 AI Career Advisor (Free using Gemini)")

name = st.text_input("Your Name")
education = st.selectbox(
    "Education Level",
    ["School (9–12)", "Diploma", "Undergraduate", "Postgraduate"]
)
interest = st.text_input("Your Interests (e.g. AI, Business, Design)")
skills = st.text_area("Your Skills (e.g. Python, Math, Communication)")
goal = st.selectbox("Career Goal", ["Job", "Startup", "Higher Studies", "Undecided"])

if st.button("Get Career Advice"):
    prompt = f"""
You are a helpful career advisor for students in India.

Student details:
Name: {name}
Education: {education}
Interests: {interest}
Skills: {skills}
Goal: {goal}

Give:
1. 3 suitable career options
2. Why each fits
3. A 6–12 month roadmap
4. Skills to learn
"""

    response = model.generate_content(prompt)
    st.write(response.text)
