import streamlit as st
import gemini_service
import json

def init_session_state():
    if "view" not in st.session_state:
        st.session_state.view = "upload"
    if "context" not in st.session_state:
        st.session_state.context = ""
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "generated_data" not in st.session_state:
        st.session_state.generated_data = None


def clear_data():
    st.session_state.generated_data = None
    st.session_state.answers = {}

def render_siderbar():
    st.sidebar.title("Study Forge")

    st.session_state.mode = st.sidebar.radio(
        "Study Mode", 
        ["Standard Guide", "Interactive Flashcard", "Exam Simulator"],
        on_change=clear_data
    )
    st.session_state.className = st.sidebar.text_input("Class Name")
    st.session_state.context = st.sidebar.text_area("Insert syllabus context/ core objective")

def render_upload_screen():
    st.title("Recall Engine")
    upload_file = st.file_uploader("Upload PDF, JPEG, etc...", type=["pdf", "txt", "png", "jpg"])

    if st.button("Generate your study guide"):
        with st.spinner("Forging your study guide..."):
            file_bytes = None
            mime_type = None

            if upload_file is not None:
                file_bytes = upload_file.getvalue()
                mime_type = upload_file.type

            st.session_state.generated_data = gemini_service.generate_study_guide(
                course_mode=st.session_state.mode,
                course_context=st.session_state.context,
                course_className=st.session_state.className,
                course_assessment=st.session_state.assessment,
                file_bytes=file_bytes,
                mime_type=mime_type
            )
            st.success("Study time!")

    if st.session_state.generated_data:
        generated_text = st.session_state.generated_data

        if st.session_state.mode == "Interactive Flashcard":
            try:
                clean_text = generated_text.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
                flashcard_data = json.loads(clean_text)

                for i, card in enumerate(flashcard_data['flashcards']):
                    st.markdown(f"**{card['question']}**")
                    with st.expander("Reveal Answer"):
                        st.write(card['answer'])
            except Exception as e:
                st.error("The AI is glitching. Please try again!")
                st.write("Output for debugging: ", generated_text)
                
        elif st.session_state.mode == "Exam Simulator":
            try:
                clean_text = generated_text.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
                exam_data = json.loads(clean_text)

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader("Assessment")
                    for i, q_data in enumerate(exam_data['exam']):
                        st.markdown(f"**{i+1} - {q_data['question']}**")
                        st.session_state.answers[i] = st.radio(
                            label="select an answer:",
                            options=q_data['options'],
                            key=f"q_{i}",
                            label_visibility="collapsed",
                            index=None
                        )
                        st.divider()
        
                with col2:
                    st.subheader("Controls")
                    submit_clicked = st.button('Submit Exam')
                    
                    if submit_clicked:
                        score = 0
                        total_questions = len(exam_data['exam'])
                        
                        for i, q_data in enumerate(exam_data['exam']):
                            user_choice = st.session_state.answers.get(i)
                            correct_letter = q_data['correct_answer']
                            
                            if user_choice and user_choice.startswith(correct_letter):
                                score += 1
                                
                        st.metric(label="Final Score", value=f"{score} / {total_questions}")

                if submit_clicked:
                    with st.expander("Review Explanations"):
                        for i, q_data in enumerate(exam_data['exam']):
                            st.write(f"**Q{i+1}:** {q_data['explanation']}")
                            st.divider()

            except Exception as e:
                st.error("The AI is glitching. Please try again!")
                st.write("Output for debugging: ", generated_text)
        else:
            st.write(generated_text)

init_session_state()
render_siderbar()

if st.session_state.view == "upload":
    render_upload_screen()