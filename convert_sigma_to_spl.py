import os
import subprocess

def customize_spl(spl_query):
    replacements = {
        'cs-method': 'method',
        'cs-status': 'status',
        # Add more replacements as needed
    }
    for old, new in replacements.items():
        spl_query = spl_query.replace(old, new)
    return spl_query



def convert_sigma_directory_to_spl(sigma_rules_dir, output_dir):
    """
    Convert all Sigma rules in the provided directory to SPL and save the output.

    Args:
        sigma_rules_dir (str): Path to the directory containing Sigma rules.
        output_dir (str): Path to the output directory for saving SPL queries.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Function to convert Sigma rule to SPL using sigmac
    def convert_sigma_to_spl(sigma_file):
        try:
            result = subprocess.run(
                ['sigma', 'convert', '-t', 'splunk', '-p', 'sysmon', sigma_file],
                capture_output=True,
                text=True,
                check=True
            )
            spl_query = result.stdout.strip()
            return customize_spl(spl_query)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {sigma_file}: {e}")
            print(f"stderr: {e.stderr}")
            return None

    # Recursively walk through the directory
    for root, _, files in os.walk(sigma_rules_dir):
        for file in files:
            if file.endswith('.yml'):
                sigma_file_path = os.path.join(root, file)
                print(f"Processing {sigma_file_path}...")
                spl_query = convert_sigma_to_spl(sigma_file_path)
                if spl_query:
                    output_file_path = os.path.join(output_dir, file.replace('.yml', '.spl'))
                    with open(output_file_path, 'w') as f:
                        f.write(spl_query)
                    print(f"Converted {sigma_file_path} to {output_file_path}")
                else:
                    print(f"Failed to convert {sigma_file_path}")

# Example usage in another script:
# from your_module import convert_sigma_directory_to_spl
# convert_sigma_directory_to_spl('./sigma/rules/windows/powershell/powershell_script', './spl_queries')

