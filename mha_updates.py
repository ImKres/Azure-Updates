from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pytz  
import os

# URL for the Microsoft Hosted Agent source code commits
MHA_URL = "https://github.com/actions/runner-images/commits/main/images/linux/Ubuntu2004-Readme.md"

# Placeholder for Teams Incoming Webhook URL
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK_MHA")

def get_latest_commit_time(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    time_tag = soup.find('relative-time')
    if time_tag is None:
        raise Exception(f"Failed to find timestamp in {url}")

    timestamp_str = time_tag.attrs.get("datetime", "")
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

        mha_timestamp = get_latest_commit_time(MHA_URL)

        mha_updated = mha_timestamp > twenty_four_hours_ago

        if mha_updated:
            message = "Microsoft Hosted Agent source code has been updated in the last 24 hours."
        else:
            message = "There have been no updates to the Microsoft Hosted Agent source code in the last 24 hours."

        send_teams_notification(message)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        send_teams_notification(error_message)

if __name__ == "__main__":
    check_for_updates()
