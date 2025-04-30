import requests
from bs4 import BeautifulSoup
import time
from irc import client
import ssl
import irc.bot
import irc.strings
import logging

# Enable debug logging
#logging.basicConfig(level=logging.DEBUG)

# Replace these with your actual values
USERNAME = "omygaz"  # all lowercase
OAUTH_TOKEN = "oauth:n2wg2bafukpii04hius7z6vkxdg6tc"
CHANNEL = "#omygaz"  # must start with #
PORT = 6667

URL = "https://nbq.gerhard.dev/16168"
OUTPUT_FILE = "list_items.txt"
INTERVAL = 60  # seconds

def fetch_list_items(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".list-group-item")

        if not items:
            return ["No list items found."]
        
        return [item.get_text(strip=True) for item in items]
    except Exception as e:
        return [f"Error fetching data: {e}"]

def update_file_loop():
    while True:
        list_items = fetch_list_items(URL)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for item in list_items:
                f.write(item + '\n')
        print("Updated list_items.txt")
        time.sleep(INTERVAL)

def on_connect(connection, event):
    print("Connected to Twitch chat.")
    connection.join(CHANNEL)

def on_join(connection, event):
    print(f"Joined {CHANNEL}.")
    # Correct indentation of the next line


def on_pubmsg(connection, event):
    print(f"{event.source.nick}: {event.arguments[0]}")
    connection.privmsg(CHANNEL, "LOOK I HAVE NO HANDS AT ALL")

def main():
	reactor = client.Reactor()
	server = "irc.chat.twitch.tv"
	try:
		conn = reactor.server().connect(server, port=PORT, nickname=USERNAME, password=OAUTH_TOKEN)
		conn.add_global_handler("welcome", on_connect)
		conn.add_global_handler("pubmsg", on_pubmsg)
		conn.join(CHANNEL)
		reactor.process_forever()
	except client.ServerConnectionError as e:
		print("❌ Connection error:", e)
	return

if __name__ == "__main__":
	main()




