import streamlit as st

def init_session_state():

    if "view" not in st.session_state:
        st.session_state.view = "upload"

def render_siderbar():
    st.sidebar.title("Sidebar menu")
    st.sidebar.text_input("Class Name")
    st.sidebar.text_input("Assessment Type (quiz or final)")
    st.sidebar.text_area("Insert syllabus context/ core objective")

def render_upload_screen():
    st.title("Recall Engine")
    st.file_uploader("Upload PDF, JPEG, whatever here...", type=["pdf", "txt", "png", "jpg"])

    if st.button("Generate your study guide"):
        st.info("Pulling you request now")

init_session_state()
render_siderbar()

if st.session_state.view == "upload":
    render_upload_screen()