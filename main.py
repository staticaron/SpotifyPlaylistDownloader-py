import spotipy
import dotenv
import os
import sys
import youtube_dl

dotenv.load_dotenv()

class Track:
    name:str
    artist:str

    def __init__(self, name, artist):
        self.artist = artist
        self.name = name

class Track_Loader:

    tracks = []

    def load_tracks(self, track_data:dict):

        all_tracks = track_data["items"]

        for data in all_tracks:
            track_name = data["track"]["name"], 
            track_artist = " ".join([artist["name"] for artist in data["track"]["artists"]])

            self.tracks.append(Track(track_name[0], track_artist))

def main():

    arg_len = len(sys.argv)

    if arg_len < 2:
        print("~~~~Give a playlist url~~~~")
        return

    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    sp_cred : spotipy.SpotifyClientCredentials = spotipy.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    client = spotipy.Spotify(auth_manager=sp_cred)

    url = sys.argv[1]
    url_prefix = "https://open.spotify.com/playlist/"

    """6WQPQSR87zB3WvYRuUimXX"""

    if url_prefix in url:
        pl = client.playlist(playlist_id=url.removeprefix(url_prefix))

        track_loader : Track_Loader = Track_Loader()
        track_loader.load_tracks(pl["tracks"])

        for i in track_loader.tracks:
            query = f"{i.artist} - {i.name} Lyrics".replace(":", "").replace("\"", "")

            download_location = '/'.join(os.getcwd().split('/')[:3]) + '/downloads/{}'.format(pl["name"])

            ydl_opts = {
                'format': 'bestaudio/best',
                'default_search': 'ytsearch',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                "outtmpl" : download_location + '/%(title)s.%(ext)s'
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading {i.name} by {i.artist}....")
                try:
                    ydl.download([query])
                except Exception as e:
                    print(f"Error occurred while downloading {i.name}")
                    continue

    else:
        print("Invalid Playlist Link. Try again!")
        return;

if __name__ == "__main__":
    main()