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

curMessage = "Start"

def on_connect(connection, event):
	print("Connected to Twitch chat.")
	connection.join(CHANNEL)

def on_join(connection, event):
	print(f"Joined {CHANNEL}.")
	# Correct indentation of the next line

def on_pubmsg(connection, event):
	global curMessage
	message = f"{event.source.nick}: {event.arguments[0]}"
	print(message)
	curMessage = message

#    connection.privmsg(CHANNEL, "LOOK I HAVE NO HANDS AT ALL")

def connectToChat():
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
	connectToChat()




