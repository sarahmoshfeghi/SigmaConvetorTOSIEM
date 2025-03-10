# Sigma Automation Project

## Overview

The Sigma Automation Project automates the process of converting Sigma rules to AQL and SPL formats, updating Sigma rules based on YAML files, and integrating them with Splunk and QRadar. This repository contains scripts for the automatic creation of rules, alerts, and the scheduling of rule updates, making it a comprehensive solution for handling Sigma-based alerts in security systems.

## Project Structure

### convert_sigma_to_aql.py
- **Date Created:** Mar 9, 2025
- **Description:** Converts Sigma rules into AQL format, enabling integration with security systems that use AQL queries.

### convert_sigma_to_spl.py
- **Date Updated:** Mar 10, 2025
- **Description:** Converts Sigma rules into SPL format for use in Splunk. This script updates the conversion process for better compatibility with Splunk's query language.

### convert_to_zip.py
- **Date Created:** Mar 9, 2025
- **Description:** Converts files into a ZIP format, providing a utility for packing files for distribution or storage.

### create_splunk_alert_ssh.py
- **Date Updated:** Mar 10, 2025
- **Description:** This script creates alerts in Splunk via SSH, ensuring secure communication when setting up Splunk alerts.

### create_splunk_rule_api.py
- **Date Created:** Mar 10, 2025
- **Description:** Allows for automated rule creation in Splunk using the Splunk API, facilitating rule management in a streamlined way.

### get_sigma_alert_update.py
- **Date Updated:** Mar 9, 2025
- **Description:** Updates Sigma alerts, ensuring the system is kept up to date with the latest rule sets and configurations.

### get_sigma_update.py
- **Date Created:** Mar 9, 2025
- **Description:** Fetches the latest Sigma rule updates, enabling automated synchronization of rule sets.

### get_sigma_update_DBBased.py
- **Date Created:** Mar 10, 2025
- **Description:** Fetches Sigma rule updates from a database, making it easier to manage rules stored in a centralized repository.

### sigma_automation.service
- **Date Created:** Mar 9, 2025
- **Description:** A system service that automates the scheduling and update of Sigma rules, ensuring continuous integration of rule changes into security systems.

### sigmascheduler.py
- **Date Updated:** Mar 9, 2025
- **Description:** This script manages the scheduling of Sigma rule updates, converting rules into AQL and SPL formats. It also integrates rule creation in QRadar based on new Sigma alerts. Additionally, it handles the Git clone process to fetch updated Sigma rules and integrates them with Splunk and QRadar through SSH or API tokens.

## Features

- **Sigma Rule Conversion:** Converts Sigma rules to AQL or SPL formats for integration with various security systems like Splunk and QRadar.
- **Alert Management:** Creates Splunk alerts via SSH or API token, providing secure and automated alert creation.
- **Sigma Rule Updates:** Automatically fetches and updates Sigma rules from YAML files, Git repositories, or a database.
- **QRadar Integration:** Automatically creates QRadar rules based on new Sigma alerts, streamlining integration with the QRadar platform.
- **Automation and Scheduling:** Schedules automated updates and conversions of Sigma rules, ensuring security systems are up to date.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
