import streamlit as st
from scripts.datapreparation import get_links_from_repo, code_docs_assessor, run_wget, clone_or_update_repo
import pandas as pd
import threading

def update_repo_list(new_url):
    try:
        df = pd.read_csv('repo_status.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['URL', 'Status'])

    if not df[df['URL'] == new_url].empty:
        st.warning("URL already exists in the list.")
        return

    df = df.append({'URL': new_url, 'Status': 'Initiated'}, ignore_index=True)
    df.to_csv('repo_status.csv', index=False)

def update_status(url, new_status):
    df = pd.read_csv('repo_status.csv')
    df.loc[df['URL'] == url, 'Status'] = new_status
    df.to_csv('repo_status.csv', index=False)

def display_status_cards():
    try:
        df = pd.read_csv('data/repo_status.csv')
        for _, row in df.iterrows():
            st.info(f"URL: {row['URL']} - Status: {row['Status']}")
    except FileNotFoundError:
        st.write("No repositories added yet.")

def process_url(url):
    readthedocs_links,readthedocs_links_clean = get_links_from_repo(url)
    injestion_type = code_docs_assessor(url,readthedocs_links,readthedocs_links_clean)
    download_path = "./data/downloads/"
    if injestion_type == 'repo':
        downloadedpath_repo = clone_or_update_repo(url, download_path)
        update_status(url, 'Ingested')
    else:
        downloadedpath_docs = run_wget(readthedocs_links_clean[0], download_path)
        downloadedpath_repo = clone_or_update_repo(url, download_path)
        update_status(url, 'Ingested')

    

def handle_url_submission(url):
    update_repo_list(url)
    threading.Thread(target=process_url, args=(url,)).start()
    

def add_repo_page():
    st.header("Add Repo")
    user_input = st.text_input("Paste the GitHub Repository Link Here:")

    if st.button("Submit"):
        handle_url_submission(user_input)

    st.markdown(
        """
        ##### Casper will attempt to ingest

        <div style="color: green;">
            <p>✅ Readthedocs page if available</p>
            <p>✅ All python files and notebooks from the repo</p>
        </div>
        <div style="color: blue;">
            <p>ℹ️ Coming soon: Git changes</p>
            <p>ℹ️ Coming soon: Git issues</p>
        </div>
        """,
        unsafe_allow_html=True
    )



    display_status_cards()

st.sidebar.title("Casper")

with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. ✅ Verify if the repo is available or ➕ Add if not \n"  # noqa: E501
            "2. 💬 Explore, understand and probe repo(s)\n"
            "3. 🔍 Debug an existing implementation of repo\n"
            "4. 👩‍💻 Implement and take to prod\n"
        )

page = st.sidebar.radio("Go to", ('Add Repo', 'Talk to a Repo', 'Debug', 'Implement'))

if page == 'Add Repo':
    add_repo_page()


