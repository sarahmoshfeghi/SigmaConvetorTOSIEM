import os
import subprocess

def convert_sigma_directory_to_aql(sigma_rules_dir, output_dir):
    """
    Convert all Sigma rules in the provided directory to AQL and save the output.

    Args:
        sigma_rules_dir (str): Path to the directory containing Sigma rules.
        output_dir (str): Path to the output directory for saving AQL queries.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Function to convert Sigma rule to AQL using sigma
    def convert_sigma_to_aql(sigma_file):
        try:
            result = subprocess.run(
                ['sigma', 'convert', '-t', 'q_radar_aql', '-p', 'qradar-aql-payload', sigma_file],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
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
                aql_query = convert_sigma_to_aql(sigma_file_path)
                if aql_query:
                    output_file_path = os.path.join(output_dir, file.replace('.yml', '.aql'))
                    with open(output_file_path, 'w') as f:
                        f.write(aql_query)
                    print(f"Converted {sigma_file_path} to {output_file_path}")
                else:
                    print(f"Failed to convert {sigma_file_path}")

# Example usage in another script:
# from your_module import convert_sigma_directory_to_aql
# convert_sigma_directory_to_aql('./sigma/rules', './aql_queries')
