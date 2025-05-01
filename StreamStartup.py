import signal
import sys
import threading
from multiprocessing.spawn import get_command_line
import requests
from bs4 import BeautifulSoup
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import socket
import shutil

from test import connectToChat

URL = "https://nbq.gerhard.dev/16168"
OUTPUT_QUEUE_FILE = "list_items.txt"
OUTPUT_SPOTIFY_FILE = "spotify_info.txt"
INTERVAL = 10  # seconds



# GUI ------------

def fetch_list_items(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".list-group-item")

        if not items:
            return ["Queue Empty"]

        return [item.get_text(strip=True) for item in items]
    except Exception as e:
        return [f"Error fetching data: {e}"]

def update_spotify_loop():
    while True:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="524c7ec66091471ebe3ab05030eaffc0",
            client_secret="9bbb422b5b5042b0834b929874512add",
            redirect_uri="https://127.0.0.1:8888/callback",
            scope="user-read-currently-playing user-read-playback-state"
        ))
        current = sp.current_playback()
        if current and current.get("is_playing"):
            song = f"{current['item']['name']} - {current['item']['artists'][0]['name']}"
            print(formatSongName(song))
            with open(OUTPUT_SPOTIFY_FILE, 'w+', encoding='utf-8') as f:
                print(["REEED", f.read(), formatSongName(song)])
                if f.read() != formatSongName(song):
                    f.write(formatSongName(song))
                    print("Updated spotify_info.txt")
        else:
            with open(OUTPUT_SPOTIFY_FILE, 'w+', encoding='utf-8') as f:
                if f.tell() != 0:
                    f.write("")
                    print("Updated spotify_info.txt")


        # list_items = fetch_list_items(URL)
        # with open(OUTPUT_QUEUE_FILE, 'w', encoding='utf-8') as f:
        #     for item in list_items:
        #         f.write(item + '\n')
        # print("Updated list_items.txt")

        time.sleep(INTERVAL)

def formatSongName(name):
    return "Listening Now: " + name

def update_queue_loop():
    while True:
        list_items = fetch_list_items(URL)
        with open(OUTPUT_QUEUE_FILE, 'w', encoding='utf-8') as f:
            for item in list_items:
                f.write(item + '\n')
        print("Updated list_items.txt")
        time.sleep(INTERVAL)



chatThread = threading.Thread(target=connectToChat)
queueThread = threading.Thread(target=update_queue_loop)
spotifyThread = threading.Thread(target=update_spotify_loop)


if __name__ == "__main__":
    chatThread.start()
    spotifyThread.start()
    queueThread.start()
