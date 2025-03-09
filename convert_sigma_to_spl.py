
import os
import subprocess

# Directory containing Sigma YAML rules
sigma_rules_dir = '/pathtotheyamlfile/yamlfile'
# Output directory for SPL queries
output_dir = '/pathtotheyamlfile/spl_queries'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to replace fields in SPL query
def customize_spl(spl_query):
    replacements = {
        'cs-method': 'method',
        # Add more replacements as needed
    }
    for old, new in replacements.items():
        spl_query = spl_query.replace(old, new)
    return spl_query

# Function to convert a Sigma rule to SPL using the sigma tool
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

# Recursively walk through the directory to find YAML files
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
