import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

URL = getenv("MUSIXMATCH_URL")
KEY = getenv("MUSIXMATCH_KEY")
MATCHER_SUBPATH = "matcher.track.get"
LYRICS_SUBPATH = "track.lyrics.get"

assert URL and KEY


def intro_lyrics(title: str, artist: str) -> str:
    id = requests.get(
        URL + MATCHER_SUBPATH,
        params={
            "apikey": KEY,
            "q_artist": artist,
            "q_track": title,
        },
    ).json()["message"]["body"]["track"]["track_id"]

    assert isinstance(id, int)

    lyrics = requests.get(
        URL + LYRICS_SUBPATH, params={"apikey": KEY, "track_id": id}
    ).json()["message"]["body"]["lyrics"]["lyrics_body"]

    return lyrics
