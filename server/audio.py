from yt_dlp import YoutubeDL

OPTIONS = {
    "format": "wav/bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
}


def download_audio(url: str) -> None:
    with YoutubeDL(OPTIONS) as ydl:
        error_code = ydl.download([url])
