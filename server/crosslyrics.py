import utils as utils
import numpy as np
import karoke

from lyrics import timestamped_lyrics
from audio import download_audio


def generate(
    youtube_url: str, track_id: str, n: int = 5, tta: bool = True
) -> tuple[float, np.ndarray, list[np.ndarray]]:
    # Audio
    info = download_audio(youtube_url)
    sr, x = utils.read(info["file"])
    x = x.astype(np.float32)

    # Lyrics
    times, lines = np.array(
        [[t, l] for t, l in timestamped_lyrics(track_id) if "(" and ")" not in l]
    ).T  # [ms], [lyric]
    times = (times.astype(int) * (sr / 1000)).astype(int)  # [samples]
    lines = lines.astype(str, copy=False)

    # Sample indices for n lyric triplets
    rand_i = np.random.choice(lines.size - 3, n)  # i, i + 1, i + 2

    return (
        sr,
        np.stack(
            (lines[rand_i], lines[rand_i + 1], lines[rand_i + 2])
        ).T,  # Lyric triplets
        [
            np.concatenate(
                (
                    x[times[i] : times[i + 1]],
                    karoke.remove_vocals(x[times[i + 1] : times[i + 2]].T, tta).astype(
                        np.float32
                    ),
                    x[times[i + 2] : times[i + 3]],
                ),
            ).T
            for i in rand_i
        ],  # Concatenated triplets of samples
    )


if __name__ == "__main__":
    sr, lyrics, samples = generate(
        "https://www.youtube.com/watch?v=asew9BF1wdw",
        "2Zo1PcszsT9WQ0ANntJbID",
        tta=False,
    )

    print(sr, lyrics)
