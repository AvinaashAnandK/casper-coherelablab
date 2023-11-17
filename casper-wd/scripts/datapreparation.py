import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import subprocess
import os
import shutil
import urllib.parse
from datetime import datetime
from git import Repo

def get_links_from_repo(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"An error occurred: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)

    readthedocs_links = [link['href'] for link in links if 'readthedocs.io' in link['href']]

    readthedocs_links_clean = []
    
    for link in readthedocs_links:
        test = urlparse(link)
        base_url = f"{test.scheme}://{test.netloc}/"
        readthedocs_links_clean = set()
        readthedocs_links_clean.add(base_url)

    return readthedocs_links,readthedocs_links_clean

def code_docs_assessor(url,readthedocs_links,readthedocs_links_clean):
    repo = urlparse(url).path.split('/')
    new_repo = []

    for link in repo:
        if link != '':
            new_repo.append(link.lower())

    readthedocs_flag = 0

    for name in new_repo:
        for link in readthedocs_links_clean:
            if name in link:
                readthedocs_flag = 1

    if readthedocs_flag == 0:
        return 'repo'
    else:
        return 'docs'

def run_wget(url, path):
    parsed_url = urllib.parse.urlparse(url)
    safe_folder_name = urllib.parse.quote_plus(parsed_url.netloc + parsed_url.path)
    download_folder = os.path.join(path, safe_folder_name)
    safe_filename = urllib.parse.quote_plus(url) + ".html"
    full_file_path = os.path.join(download_folder, safe_filename)
    history_file_path = os.path.join(path, "fluffydownloadhistory.txt")

    # Current time for logging
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_stamp = datetime.now().strftime("%Y%m%d")

    # Check if the URL has already been downloaded
    if is_url_downloaded(history_file_path, url):
        # Move existing download to archived folder
        archived_folder = os.path.join(path, "archived", date_stamp + "_" + safe_folder_name)
        os.makedirs(os.path.dirname(archived_folder), exist_ok=True)
        shutil.move(download_folder, archived_folder)

    try:
        # Ensure download folder exists
        os.makedirs(download_folder, exist_ok=True)

        # Run the wget command with output redirected to the specific file
        subprocess.run(['wget', '-r', '-A.html', '-P', full_file_path, url], check=True)

        # Update the download history
        update_download_history(history_file_path, url, current_time)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running wget: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def is_url_downloaded(history_file_path, url):
    if not os.path.exists(history_file_path):
        return False
    with open(history_file_path, 'r') as file:
        return url in file.read()

def update_download_history(history_file_path, url, current_time):
    with open(history_file_path, 'a') as file:
        file.write(f"URL: {url}\nDownloaded On: {current_time}\n\n")

def clone_or_update_repo(repo_url, path):
    parsed_url = urllib.parse.urlparse(repo_url)
    safe_folder_name = urllib.parse.quote_plus(parsed_url.netloc + parsed_url.path)
    repo_folder = os.path.join(path, safe_folder_name)
    history_file_path = os.path.join(path, "fluffydownloadhistory.txt")

    # Current time for logging
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_stamp = datetime.now().strftime("%Y%m%d")

    # Check if the URL has already been cloned
    if os.path.exists(repo_folder):
        # Move existing repo to archived folder
        archived_folder = os.path.join(path, "archived", date_stamp + "_" + safe_folder_name)
        os.makedirs(os.path.dirname(archived_folder), exist_ok=True)
        shutil.move(repo_folder, archived_folder)

    try:
        # Clone the repo
        Repo.clone_from(repo_url, repo_folder)
        print(f"Repository cloned successfully to {repo_folder}")

        # Update the download history
        update_download_history(history_file_path, repo_url, current_time)
    except Exception as e:
        print(f"An error occurred while cloning the repo: {e}")
