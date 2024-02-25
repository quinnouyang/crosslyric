from yt_dlp import YoutubeDL

OPTIONS = {
    "format": "wav/bestaudio/best",
    "outtmpl": "./%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
}


def download_audio(url: str) -> dict[str, str]:
    with YoutubeDL(OPTIONS) as ydl:
        info = ydl.extract_info(url)
        assert info

        return {
            "artist": info["uploader"],
            "title": info["title"],
            "file": info["title"] + ".wav",
        }


if __name__ == "__main__":
    print(download_audio("https://www.youtube.com/watch?v=asew9BF1wdw"))
