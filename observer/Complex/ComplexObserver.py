import requests
from bs4 import BeautifulSoup
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

# Enter the profile url you want to observe
url = 'https://www.kogama.com/profile/ID/'

# Enter the webhook URL where the data will be sent
WEBHOOK_URL = 'Webhook'

# Initial scraping to get the current data
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
username = soup.find('div', {'class': 'username'}).text.strip()
profile_url = f'<{url}>'

description_container = soup.find('div', {'class': 'description-container'})
if description_container is None:
    description_text = 'No description provided'
else:
    description_text = description_container.find('div', {'class': 'text'}).text.strip()

xp_container = soup.find('div', {'class': 'xp progression-item'})
if xp_container is None:
    xp_text = 'N/A'
else:
    xp_text = xp_container.find('div', {'class': 'data'}).text.strip()

rank_container = soup.find('div', {'class': 'rank progression-item'})
if rank_container is None:
    rank_text = 'N/A'
else:
    rank_text = rank_container.find('div', {'class': 'data'}).text.strip()

# Set up the initial embed message
embed = DiscordEmbed(title=f'{username} Kogama Profile', url=url, color='FF5733')
embed.add_embed_field(name='Description', value=description_text)
embed.add_embed_field(name='XP', value=xp_text)
embed.add_embed_field(name='Rank', value=rank_text)

webhook = DiscordWebhook(url=WEBHOOK_URL)
webhook.add_embed(embed)
webhook.execute()

# Loop through and check for changes every 20 seconds
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description_container = soup.find('div', {'class': 'description-container'})
    if description_container is None:
        description_text_new = 'No description provided'
    else:
        description_text_new = description_container.find('div', {'class': 'text'}).text.strip()
        
    xp_container = soup.find('div', {'class': 'xp progression-item'})
    if xp_container is None:
        xp_text_new = 'N/A'
    else:
        xp_text_new = xp_container.find('div', {'class': 'data'}).text.strip()

    rank_container = soup.find('div', {'class': 'rank progression-item'})
    if rank_container is None:
        rank_text_new = 'N/A'
    else:
        rank_text_new = rank_container.find('div', {'class': 'data'}).text.strip()

    if description_text_new != description_text or xp_text_new != xp_text or rank_text_new != rank_text:
        description_text = description_text_new
        xp_text = xp_text_new
        rank_text = rank_text_new
        embed = DiscordEmbed(title=f'{username} Kogama Profile Updated', url=url, color='FF5733')
        embed.add_embed_field(name='Description', value=description_text)
        embed.add_embed_field(name='XP', value=xp_text)
        embed.add_embed_field(name='Rank', value=rank_text)
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        webhook.add_embed(embed)
        webhook.execute()

    time.sleep(20) # Wait for 20 seconds before checking again
