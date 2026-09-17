import streamlit as st
import gemini_service

def init_session_state():

    if "view" not in st.session_state:
        st.session_state.view = "upload"

    if "context" not in st.session_state:
        st.session_state.context = ""

def render_siderbar():
    st.sidebar.title("Sidebar menu")
    st.sidebar.text_input("Class Name")
    st.sidebar.text_input("Assessment Type (quiz or final)")

    st.session_state.context = st.sidebar.text_area("Insert syllabus context/ core objective")

def render_upload_screen():
    st.title("Recall Engine")
    st.file_uploader("Upload PDF, JPEG, whatever here...", type=["pdf", "txt", "png", "jpg"])

    if st.button("Generate your study guide"):

        with st.spinner("Forging your study guide..."):

            generated_text = gemini_service.generate_study_guide(st.session_state.context)

            st.success("study time!")
            st.write(generated_text)

init_session_state()
render_siderbar()

if st.session_state.view == "upload":
    render_upload_screen()