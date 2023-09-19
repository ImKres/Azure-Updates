# Azure CLI, Azure PowerShell & Microsoft Hosted Agent Updates Notifier
A Python script that automatically checks for updates in Azure CLI, Azure PowerShell, and Microsoft's hosted agent for Ubuntu 20.04. Notifications are sent to a Microsoft Teams channel via an incoming webhook.

## Features:
Fetches the latest release information from GitHub for Azure CLI and Azure PowerShell.
Checks the last modified time for Microsoft's hosted agent for Ubuntu 20.04.
Sends a notification message to a Microsoft Teams channel.
Designed to run daily via GitHub Actions.

## How to Use:
Clone this repository.
Add your Microsoft Teams webhook URL in the Python script.
(Optional) Add your GitHub token in the Python script for API authentication.
Set up the GitHub Actions YAML to run the script on a schedule.
Monitor your Teams channel for daily updates!

## Dependencies:
Python 3.x
requests package
BeautifulSoup package
pytz package
