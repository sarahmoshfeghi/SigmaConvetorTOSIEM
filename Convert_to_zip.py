
import os
import shutil
import subprocess

def zip_output_directory(output_dir, zip_file):
    """
    Zips the contents of the output directory, replaces the existing zip file if it exists,
    and ensures the zip file has read permissions.

    Args:
        output_dir (str): Path to the directory to be zipped.
        zip_file (str): Path to the zip file that will be created.

    Returns:
        None
    """
    # Check if the zip file already exists, and remove it if it does
    if os.path.exists(zip_file):
        os.remove(zip_file)  # Remove the old zip file to replace it

    # Create a zip file from the output directory
    shutil.make_archive(zip_file.replace('.zip', ''), 'zip', output_dir)
    print(f"Zipped the output directory to {zip_file}")

    # Ensure the zip file has read permissions
    try:
        subprocess.run(["chmod", "+r", zip_file], check=True)
        print(f"Added read permission to {zip_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set permissions on {zip_file}: {e}")

