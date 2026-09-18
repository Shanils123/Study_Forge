import streamlit as st
import gemini_service
import json

def init_session_state():

    if "view" not in st.session_state:
        st.session_state.view = "upload"

    if "context" not in st.session_state:
        st.session_state.context = ""

def render_siderbar():
    st.sidebar.title("Study Forge")

    st.session_state.mode = st.sidebar.radio("Study Mode" , ["Standard Guide", "Interactive Flashcard"])
    st.session_state.className = st.sidebar.text_input("Class Name")
    st.session_state.assessment = st.sidebar.text_input("Assessment Type (quiz or final)")
    st.session_state.context = st.sidebar.text_area("Insert syllabus context/ core objective")

def render_upload_screen():
    st.title("Recall Engine")
    upload_file = st.file_uploader("Upload PDF, JPEG, whatever here...", type=["pdf", "txt", "png", "jpg"])

    if st.button("Generate your study guide"):

        with st.spinner("Forging your study guide..."):

            file_bytes = None
            mime_type = None

            if upload_file is not None:
                file_bytes = upload_file.getvalue()
                mime_type = upload_file.type

            generated_text = gemini_service.generate_study_guide(
                course_mode =st.session_state.mode,
                course_context=st.session_state.context,
                course_className=st.session_state.className,
                course_assessment=st.session_state.assessment,
                file_bytes=file_bytes,
                mime_type=mime_type)


            st.success("study time!")

            if st.session_state.mode == "Interactive Flashcard":
                try:
                    clean_text = generated_text.replace("```JSON", "").replace("```", "").strip()

                    flashcard_data = json.loads(clean_text)

                    for i, card in enumerate(flashcard_data['flashcards']):
                        st.markdown(f"**{card['question']}**")
                        with st.expander("Reveal Answer"):
                            st.write(card['answer'])
                except Exception as e:

                    st.error("The Ai is glitching. Please try again!")
                    st.write("Output for debugging: ", generated_text)
            else:
                st.write(generated_text)

init_session_state()
render_siderbar()

if st.session_state.view == "upload":
    render_upload_screen()