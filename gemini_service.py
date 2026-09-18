import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-3-flash-preview')

def generate_study_guide(course_context, course_className, course_assessment, course_mode, file_bytes=None, mime_type=None ):

    prompt = f"""
    You are an expert tutor for the course: {course_className}.
    
    Using the provided syllabus context and any attached documents, create a targeted study guide. 
    
    The user has requested the following assessment format: {course_assessment}. 
    Tailor the length, difficulty, and style of the generated quiz strictly to match this assessment type.
    
    Additional Context: {course_context}
"""
    if course_mode == "Interactive Flashcard":
        prompt += """
        CRITICAL INSTRUCTION:
        You must respond ONLY with a valid JSON object. Do not include markdown formatting blocks like ```json. 
        Use this exact structure:
        {
          "flashcards": [
            {"question": "Question text here", "answer": "Answer text here"}
          ]
        }
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