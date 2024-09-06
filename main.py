import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = "37ccd3413bcb40d2bbbf92b94f4a71d5"
Client_secret = "10a5936fc50b40499f87c35299c318f6"
redirect_uri = "https://example.com/callback"

user_input = input("Which year do you want to travel to? Type the date in this format YYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{user_input}"
response = requests.get(URL)
html_file = response.text

soup = BeautifulSoup(html_file, "html.parser")
all_songs = soup.select("li ul li h3", )

songs = [song.get_text(strip=True) for song in all_songs]

print(songs)

sp= SpotifyOAuth(
    client_id=Client_ID,
    client_secret=Client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",

)
sp_oauth = spotipy.Spotify(auth_manager=sp)

# auth_url = sp.get_authorize_url()
# print("Please go to this URL and authorize the application:")
# print(auth_url)
user_id = sp_oauth.current_user()["id"]
playlist_tracks = []
for song in songs:
    song_name = song
    year = int(user_input[:4])
    #print(year)

    queue = f"track:{song_name} year:{year}"
    result = sp_oauth.search(q=queue, type="track", limit=1)
    try:
        playlist_tracks.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print("No track found.")


playlist_name = f"{user_input} Billboard 100"
playlist_description = f"100 songs from billboard on {user_input} "

playlist = sp_oauth.user_playlist_create(user_id, name=playlist_name, description=playlist_description, public=False)

sp_oauth.playlist_add_items(playlist["id"], playlist_tracks)

print(playlist)

