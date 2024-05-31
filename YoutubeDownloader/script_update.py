import requests
import subprocess
import sys
import os

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/leodonathilic/YoutubeBulkDownloader/main/YoutubeDownloader/version.txt"
GITHUB_SCRIPT_URL = "https://raw.githubusercontent.com/leodonathilic/YoutubeBulkDownloader/main/YoutubeDownloader/youtube_dl.py"

# Path to the local version file and script
LOCAL_VERSION_FILE = "version.txt"
LOCAL_SCRIPT_FILE = "youtube_dl.py"

def get_github_version():
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()
        github_version = response.text.strip()
        return github_version
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return None

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, 'r') as file:
        local_version = file.read().strip()
        return local_version

def download_new_script():
    try:
        response = requests.get(GITHUB_SCRIPT_URL)
        response.raise_for_status()
        with open(LOCAL_SCRIPT_FILE, 'wb') as file:
            file.write(response.content)
        print("Downloaded the new script successfully.")
    except requests.RequestException as e:
        print(f"Error downloading the new script: {e}")

def update_script():
    print("Updating the script...")
    download_new_script()
    print("Update complete. Restarting the script...")
    os.execv(sys.executable, ['python'] + sys.argv)

def main():
    github_version = get_github_version()
    local_version = get_local_version()

    if not github_version:
        print("Could not check for updates.")
        return

    if not local_version or github_version > local_version:
        print(f"Update available: {github_version} (current version: {local_version})")
        choice = input("Do you want to update? (yes/no): ").strip().lower()
        if choice == 'yes':
            update_script()
        else:
            print("Skipping update.")
    else:
        print("You are already using the latest version.")

if __name__ == "__main__":
    main()
