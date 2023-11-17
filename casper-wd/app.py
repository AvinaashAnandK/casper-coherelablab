import streamlit as st
from scripts.datapreparation import get_links_from_repo, code_docs_assessor, run_wget, clone_or_update_repo

def add_repo_page():
    st.header("Add Repo")
    repo_link = st.text_input("Paste the GitHub Repository Link Here:")
    st.text("Casper will attempt to ingest the ReadTheDocs pages of the repository if available; otherwise, it will ingest the entire repository.")
    st.text("Git issues and changes to the main branch will also be incorporated.")

st.sidebar.title("Casper")

page = st.sidebar.radio("Go to", ('Add Repo', 'Talk to a Repo', 'Debug', 'Implement'))

if page == 'Add Repo':
    add_repo_page()


