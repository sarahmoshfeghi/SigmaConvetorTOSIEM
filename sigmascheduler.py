
from get_sigma_alert_update import ioc_reporter
from convert_sigma_to_spl import convert_sigma_directory_to_spl
from convert_to_zip import zip_output_directory
import schedule
import subprocess
import time
import os
import glob
import shutil
sigma_rules_dir = '/pathtoyamlfile/yamlfile'
output_dir = '/pathtothesplquery/spl_queries'
zip_file = '/pathtosplfile/splrule.zip'
recipient_email = 'emailaddress'
def clear_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Remove all .yml files in the folder
        for file in glob.glob(os.path.join(folder_path, "*.yml")):
            os.remove(file)
            print(f"Removed: {file}")

        # Remove all .spl files in the folder
        for file in glob.glob(os.path.join(folder_path, "*.spl")):
            os.remove(file)
            print(f"Removed: {file}")
        print("Folder cleanup complete.")
    else:
        print(f"The folder {folder_path} does not exist or is not a directory.")

def send_email_with_mutt(zip_file, recipient_email):
    """
    Sends an email using the mutt command with a zip file as an attachment.

    Args:
        zip_file (str): Path to the zip file to attach.
        recipient_email (str): Email address of the recipient.

    Returns:
        None
    """
    subject = "SigmaRule"
    body = "These Sigma rules have been added"

    # Run the mutt command using subprocess
    try:
        subprocess.run(
            ['echo', body, '|', 'mutt', '-s', subject, '-a', zip_file, '--', recipient_email],
            shell=True,
            check=True
        )
        print(f"Email sent to {recipient_email} with {zip_file} attached.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send email: {e}")


def job():
    print("Running scheduled task...")
    clear_folder("/pathtoymlfile/yamlfile")
    clear_folder("/pathtosplfile/spl_queries")
    ioc_reporter()
    convert_sigma_directory_to_spl(sigma_rules_dir, output_dir)
    zip_output_directory(output_dir, zip_file)
    send_email_with_mutt(zip_file,recipient_email)
    schedule.every().saturday.at("14:20").do(job)
while True:
    schedule.run_pending()
