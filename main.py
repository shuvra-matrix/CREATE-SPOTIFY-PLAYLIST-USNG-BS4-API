from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = ''
Client_Secret = ''
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:  ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"

request = requests.get(billboard_url).text

sup = BeautifulSoup(request,'html.parser')

title = sup.find_all(name ='span', class_='chart-element__information__song text--truncate color--primary')
titles = [name.getText() for name in title]
title_list = titles[::]



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:5500/",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
with open("title.txt", 'w') as title:
    for list in title_list:
        result = sp.search(q=f"track:{list} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{list} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)