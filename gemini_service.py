import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-3-flash-preview')

def generate_study_guide(course_context):

    prompt = f"""
    You are an expert tutor. Create a structured active recall study guide 
    based on the following context. Include 3 flashcards and a short quiz.
    
    Context: {course_context}
"""
    response = model.generate_content(prompt)

    return response.text