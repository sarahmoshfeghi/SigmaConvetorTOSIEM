import os
import subprocess
import requests
from urllib.parse import urlencode

def clone_repository(repo_url, target_dir):
    if not os.path.exists(target_dir):
        subprocess.run(['git', 'clone', repo_url, target_dir], check=True)
    else:
        subprocess.run(['git', '-C', target_dir, 'pull'], check=True)

def apply_spl_rules(spl_directory, splunk_url, auth_token):
    spl_files = [f for f in os.listdir(spl_directory) if f.endswith('.spl')]
    
    if not spl_files:
        print(f"No .spl files found in directory: {spl_directory}")
        return
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    for file_name in spl_files:
        file_path = os.path.join(spl_directory, file_name)
        with open(file_path, 'r') as f:
            search_query = f.read()
        
        alert_name = file_name.replace('.spl', '')
        data = {
            "name": alert_name,
            "search": search_query,
            "alert_type": "number of events",
            "alert_threshold": "0",
            "actions": "email",
            "cron_schedule": "0 6 * * 1"
        }
        
        response = requests.post(
            f"{splunk_url}/{alert_name}",
            headers=headers,
            data=urlencode(data),
            verify=False
        )
        
        if response.status_code in range(200, 300):
            print(f"Successfully applied alert: {alert_name}")
        else:
            print(f"Failed to apply alert {alert_name}: {response.text}")

def main():
    GIT_REPO_URL = 'https://my-git.example.com/sigmahq'
    SPLUNK_URL = 'https://my-splunk.com:8089/servicesNS/splunk/search/saved/searches'
    SPL_DIRECTORY = 'path/to/your/dir'
    AUTH_TOKEN = 'your-splunk-auth-token'
    
    REPO_DIR = './sigma_repo'
    
    clone_repository(GIT_REPO_URL, REPO_DIR)
    apply_spl_rules(SPL_DIRECTORY, SPLUNK_URL, AUTH_TOKEN)
    
if __name__ == "__main__":
    main()
