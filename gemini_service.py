import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-3-flash-preview')

def generate_study_guide(course_context, course_className, course_assessment, course_mode, file_bytes=None, mime_type=None):

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
            {"question": "Term or question text here", "answer": "Definition or explanation here"}
          ]
        }
        Generate exactly 15 flashcards based on the context. Ensure the question field is never empty.
        """

    elif course_mode == "Exam Simulator":
        prompt += """
        CRITICAL: You are an exam generator. You must return a raw JSON object and nothing else.
        Follow this exact schema:
        {
          "exam": [
            {
              "question": "Question text here",
              "options": ["A) First", "B) Second", "C) Third", "D) Fourth"],
              "correct_answer": "A",
              "explanation": "Brief explanation."
            }
          ]
        }
        Generate exactly 15 multiple-choice questions based on the context.
        """


    is_json = course_mode in ["Interactive Flashcard", "Exam Simulator"]
    config = {"response_mime_type": "application/json"} if is_json else {}

    if file_bytes and mime_type:
        prompt_parts = [
            prompt,
            {"mime_type": mime_type, "data": file_bytes}
        ]
        response = model.generate_content(
            contents=prompt_parts,
            generation_config=config
        )
    else:
        response = model.generate_content(
            contents=prompt,
            generation_config=config
        )

    return response.text