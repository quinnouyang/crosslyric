import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()

URL = getenv("MUSIXMATCH_URL")
KEY = getenv("MUSIXMATCH_KEY")
assert URL and KEY

parameters = {
    "apikey": KEY,
    "q_artist": "eminem",
    "page_size": 10,
    "page": 1,
    "s_artist_rating": "desc",
}

print(requests.get(URL, params=parameters).json())
