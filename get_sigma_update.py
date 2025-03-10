import os
import subprocess
from datetime import datetime, timedelta

def clone_repository(repo_url, target_dir):
    """Clone or update the Git repository."""
    if not os.path.exists(target_dir):
        subprocess.run(['git', 'clone', repo_url, target_dir], check=True)
    else:
        subprocess.run(['git', '-C', target_dir, 'pull'], check=True)

def get_recent_changes(repo_dir, days):
    """Get .yml files changed in the last given days."""
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    result = subprocess.run(
        ['git', '-C', repo_dir, 'log', f'--since={since_date}', '--name-only', '--pretty=format:', 'rules/**/*.yml'],
        capture_output=True, text=True, check=True
    )
    changed_files = set(filter(None, result.stdout.split('\n')))
    return changed_files

def send_email(subject, body, recipients, sender):
    """Send an email notification."""
    print(f"Sending email to {recipients} from {sender} with subject: {subject}")
    # Email sending logic should be implemented here

def main():
    REPO_URL = 'https://github.com/SigmaHQ/sigma'
    REPO_DIR = './sigma_repo'
    DAYS_TO_CHECK = 7
    EMAIL_RECIPIENTS = 'recipient1@example.com,recipient2@example.com'
    EMAIL_SENDER = 'sender@example.com'

    clone_repository(REPO_URL, REPO_DIR)
    changed_files = get_recent_changes(REPO_DIR, DAYS_TO_CHECK)
    if changed_files:
        print(f"Changed .yml files in the last {DAYS_TO_CHECK} days:")
        print('\n'.join(changed_files))
        send_email("New or Updated .yml Files Sigma Found", '\n'.join(changed_files), EMAIL_RECIPIENTS, EMAIL_SENDER)
    else:
        print("No new or updated .yml files found.")

if __name__ == "__main__":
    main()
