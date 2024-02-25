from pprint import pprint
from syrics.api import Spotify
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SP_DC = getenv("SPOTIFY_SP_DC")

assert SP_DC

SP = Spotify(SP_DC)


def timestamped_lyrics(id: str) -> list[tuple[int, str]]:
    return [
        (int(lines["startTimeMs"]), lines["words"])
        for lines in SP.get_lyrics(id)["lyrics"]["lines"]
    ]


if __name__ == "__main__":
    pprint(timestamped_lyrics("2Zo1PcszsT9WQ0ANntJbID"))
