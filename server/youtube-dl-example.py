from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg) -> None:
        print(msg)

    def warning(self, msg) -> None:
        print(msg)

    def error(self, msg) -> None:
        print(msg)


def my_hook(d) -> None:
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://www.youtube.com/watch?v=BaW_jenozKc"])
