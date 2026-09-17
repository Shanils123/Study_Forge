import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-3-flash-preview')

def generate_study_guide(course_context, file_bytes=None, mime_type=None ):

    prompt = f"""
    You are an expert tutor. Create a structured active recall study guide 
    based on the following context. Include 3 flashcards and a short quiz.
    
    Context: {course_context}
"""
    if file_bytes and mime_type:
        prompt_parts = [
            prompt,
            {"mime_type": mime_type, "data": file_bytes}
        ]
        response = model.generate_content(prompt_parts)
    else:

        response = model.generate_content(prompt)

    return response.text