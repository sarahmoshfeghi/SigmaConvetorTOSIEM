import paramiko
import configparser
import os


# Function to read the SPL from  a file
def read_spl_file(spl_file_path):
    try:
        with open(spl_file_path, 'r') as file:
            spl_query = file.read()
        return spl_query
    except FileNotFoundError as e:
        print(f"Error reading SPL file: {e}")
        return None


# Function to read credentials from a separate file
def read_credentials(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    ssh_host = config.get('SSH', 'host')
    ssh_username = config.get('SSH', 'username')
    ssh_password = config.get('SSH', 'password')

    return ssh_host, ssh_username, ssh_password

# Function to SSH into Splunk server and modify the savedsearches.conf file
def create_alert_via_ssh(spl_query, alert_name, ssh_host, ssh_username, ssh_password):
    # Define the path to savedsearches.conf on the Splunk server
    savedsearches_conf_path = r'Pathtothesavedsearchconfig\savedsearches.conf'

    # Define the new alert configuration
    alert_config = f"""
[{alert_name}]
action.email = 1
action.email.allow_empty_attachment = 0
action.email.include.results_link = 0
action.email.include.view_link = 0
action.email.inline = 1
action.email.sendresults = 1
action.email.to = "Emailaddress"
action.email.useNSSubject = 1
action.keyindicator.invert = 0
action.makestreams.param.verbose = 0
action.nbtstat.param.verbose = 0
action.notable.param.verbose = 0
action.nslookup.param.verbose = 0
action.ping.param.verbose = 0
action.risk.forceCsvResults = 1
action.risk.param.verbose = 0
action.send2uba.param.verbose = 0
action.threat_add.param.verbose = 0
action.webhook.enable_allowlist = 0
alert.suppress = 0
alert.track = 0
counttype = number of events
cron_schedule = 0 14 * * *
dispatch.earliest_time = -1d
dispatch.latest_time = now
display.general.type = statistics
display.page.search.mode = verbose
display.page.search.tab = statistics
enableSched = 1
quantity = 0
relation = greater than
request.ui_dispatch_app = search
request.ui_dispatch_view = search
search = {spl_query}
"""

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_username, password=ssh_password)

    # Read the current contents of savedsearches.conf
    sftp = ssh.open_sftp()
    try:
        with sftp.open(savedsearches_conf_path, 'r') as conf_file:
            current_config = conf_file.read().decode('utf-8')  # Decode bytes to string
    except FileNotFoundError:
        current_config = ""

    # Append the new alert configuration to the current config
    updated_config = current_config + "\n" + alert_config

    # Write the updated config back to savedsearches.conf
    with sftp.open(savedsearches_conf_path, 'w') as conf_file:
        conf_file.write(updated_config.encode('utf-8'))  # Encode string back to bytes

    # Close the SFTP and SSH connections
    sftp.close()
    ssh.close()

    print(f"Alert '{alert_name}' has been created in Splunk.")

# Main function
def main():
    # Path to your SPL file
    spl_directory = r'/pathtothesqlfiles/spl_queries/'

    # Path to the credentials file
    credentials_file_path = r'/pathtothesqlfiles/credentials.ini'

    # Read the SPL query from the file
    #spl_query = read_spl_file(spl_file_path)

    # Read credentials from the credentials file
    ssh_host, ssh_username, ssh_password = read_credentials(credentials_file_path)

    # Alert details
    #alert_name = "Sql Ansible Alert"

    # Create the alert by modifying savedsearches.conf
    #create_alert_via_ssh(spl_query, alert_name, ssh_host, ssh_username, ssh_password)
    create_alerts_for_spl_directory(spl_directory, ssh_host, ssh_username, ssh_password)

def create_alerts_for_spl_directory(spl_directory, ssh_host, ssh_username, ssh_password):
    for root, _, files in os.walk(spl_directory):
        for file in files:
            if file.endswith('.spl'):
                # Construct the full path to the SPL file
                spl_file_path = os.path.join(root, file)

                # Read the SPL query from the file
                spl_query = read_spl_file(spl_file_path)
                if spl_query:
                    # Generate a unique alert name based on the SPL file name (without extension)
                    alert_name = os.path.splitext(file)[0].replace(" ", "_")

                    # Create the alert in Splunk
                    create_alert_via_ssh(spl_query, alert_name, ssh_host, ssh_username, ssh_password)
                else:
                    print(f"Failed to read {spl_file_path}")


# Execute the main function
if __name__ == "__main__":
    main()
