import numpy as np
from scipy.io import wavfile


def read(path: str) -> tuple[int, np.ndarray]:
    sr, x = wavfile.read(path)
    x = x / 2**15

    return sr, x


def sound(x: np.ndarray, sr: float, label="") -> None:
    from IPython.display import display, Audio, HTML

    display(
        HTML(
            "<style> table, th, td {border: 0px; }</style> <table><tr><td>"
            + label
            + "</td><td>"
            + Audio(x, rate=sr)._repr_html_()[3:]
            + "</td></tr></table>"
        )
    )


def sounds(
    sounds: list[np.ndarray],
    sr: float | int | list[float | int],
    labels: list[str] = [],
    title="",
) -> None:
    if title:
        print(title)

    labels.extend([""] * (len(sounds) - len(labels)))

    if isinstance(sr, (float, int)):
        sr = [sr] * len(sounds)

    for x, s, l in zip(sounds, sr, labels):
        sound(x, sr=s, label=l)
