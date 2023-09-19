from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pytz  # For timezone conversion
import os

# URLs for Azure CLI and PowerShell release notes
AZURE_CLI_URL = "https://docs.microsoft.com/en-us/cli/azure/release-notes-azure-cli"
AZURE_PS_URL = "https://docs.microsoft.com/en-us/powershell/azure/release-notes-azureps?view=azps-10.3.0&viewFallbackFrom=azps-10.0.0"

# Placeholder for Teams Incoming Webhook URL
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK_AZURE")

def get_latest_release_time(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the 'time' HTML element
    time_tag = soup.find('time')

    if time_tag is None:
        raise Exception(f"Failed to find timestamp in {url}")

    # Get the 'datetime' attribute value from the 'time' element
    timestamp_str = time_tag.attrs.get("datetime", "")
    
    # Convert the timestamp string to a datetime object
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

    return timestamp

def send_teams_notification(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }
    response = requests.post(TEAMS_WEBHOOK, headers=headers, json=payload)
    response.raise_for_status()

def check_for_updates():
    try:
        utc_now = datetime.now().astimezone(pytz.utc)
        twenty_four_hours_ago = utc_now - timedelta(days=1)

        cli_timestamp = get_latest_release_time(AZURE_CLI_URL)
        ps_timestamp = get_latest_release_time(AZURE_PS_URL)

        cli_updated = cli_timestamp > twenty_four_hours_ago
        ps_updated = ps_timestamp > twenty_four_hours_ago

        if cli_updated and ps_updated:
            message = "Azure CLI & Azure PowerShell have been updated in the last 24 hours."
        elif cli_updated:
            message = "Azure CLI has been updated in the last 24 hours. No updates for Azure PowerShell."
        elif ps_updated:
            message = "Azure PowerShell has been updated in the last 24 hours. No updates for Azure CLI."
        else:
            message = "There are no updates in the last 24 hours for Azure CLI and Azure PowerShell."

        send_teams_notification(message)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        send_teams_notification(error_message)

if __name__ == "__main__":
    check_for_updates()
