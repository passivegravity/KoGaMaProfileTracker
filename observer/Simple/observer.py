import time
import requests
from bs4 import BeautifulSoup

# Replace these placeholders with your own information
profile_url = "https://www.kogama.com/profile/profileID/"
discord_webhook_url = "YourWebhook"

# Set the initial description
description = ""

while True:
    # Scrape the profile page
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, "html.parser")
    username_element = soup.find("div", {"class": "username"})
    username = username_element.text.strip() if username_element else "Unknown user"
    profile_link = profile_url
    description_container = soup.find("div", {"class": "description-container"})
    description_element = description_container.find("div", {"class": "text", "itemprop": "description"}) if description_container else None

    if description_element is None:
        # Handle the case where the description element is not found
        print("Error: could not find description element on page")
    else:
        new_description = description_element.text.strip()

        # Check for a change in the description
        if new_description != description:
            description = new_description
            embed_description = f"**[{username}](<{profile_link}>)** updated their description:\n\n{new_description}"
            message = {
                "embeds": [
                    {
                        "title": "Description Updated",
                        "description": embed_description,
                        "color": 0x00ff00
                    }
                ]
            }

            # Send a webhook message to Discord
            headers = {"Content-Type": "application/json"}
            response = requests.post(discord_webhook_url, json=message, headers=headers)

    # Wait 20 seconds before checking again
    time.sleep(20)
