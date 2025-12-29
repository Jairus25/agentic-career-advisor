import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Career Advisor", layout="centered")

st.title("🎓 AI Career Advisor for Students")

name = st.text_input("Your Name")
education = st.selectbox(
    "Education Level",
    ["School (9–12)", "Diploma", "Undergraduate", "Postgraduate"]
)
interest = st.text_input("Your Interests")
skills = st.text_area("Your Skills")
goal = st.selectbox("Career Goal", ["Job", "Startup", "Higher Studies", "Undecided"])

if st.button("Get Career Advice"):
    prompt = f"""
You are an expert career advisor for students in India.

Name: {name}
Education: {education}
Interests: {interest}
Skills: {skills}
Goal: {goal}

Suggest:
1. 3 career options
2. Roadmap
3. Skills to learn
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    st.write(response.choices[0].message.content)
