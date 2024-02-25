import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as mplaxes
from scipy import signal
from scipy.io import wavfile


def read(path: str) -> tuple[int, np.ndarray]:
    sr, x = wavfile.read(path)
    x = x / 2**15

    return sr, x


def _pad(x: np.ndarray, dft_size: int = 512, hop_size: int = 128) -> np.ndarray:
    return (
        np.pad(x, (int(np.ceil((hop_size - d) / 2)), int(np.floor((hop_size - d) / 2))))
        if (d := (x.size - dft_size) % hop_size)
        else x
    )


def _calculate_figure_size(
    nrows: int = 1,
    ncols: int = 1,
    subplot_width: int = 3,
    subplot_height: int = 2,
    min_spacing: float = 0.5,
) -> tuple[float, float]:
    return (ncols * subplot_width) + (ncols - 1) * min_spacing, (
        nrows * subplot_height
    ) + (nrows - 1) * min_spacing


def stft(
    input_sound: np.ndarray,
    dft_size: int = 512,
    hop_size: int = 128,
    window: np.ndarray | None = None,
) -> np.ndarray:
    input_sound = _pad(input_sound, dft_size, hop_size)

    if window is None:
        window = signal.windows.hamming(dft_size, sym=False)

    # Return a complex-valued spectrogram (frequencies x time)
    return np.array(
        [
            np.fft.rfft(window * input_sound[i * hop_size : i * hop_size + dft_size])
            for i in np.arange((input_sound.size - dft_size) // hop_size)  # Ew...
        ]
    ).T


def istft(
    stft_output: np.ndarray,
    dft_size: int = 512,
    hop_size: int = 128,
    window: np.ndarray | None = None,
) -> np.ndarray:
    _, n_frames = stft_output.shape
    if window is None:
        window = signal.windows.hamming(dft_size, sym=False)

    x = np.zeros(n_frames * hop_size + dft_size)
    for i in np.arange(n_frames):
        x[i * hop_size : i * hop_size + dft_size] += (
            np.fft.irfft(stft_output[:, i]) * window
        )

    return x


def sound(x: np.ndarray, sr: int, label="") -> None:
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


def specshow(
    data: np.ndarray,
    sr: int,
    dft_size: int = 512,
    hop_size: int = 128,
    ax: mplaxes.Axes | None = None,
    title: str = "",
    label_axis=True,
) -> mplaxes.Axes:
    if ax is None:
        ax = plt.gca()

    ax.pcolormesh(
        np.arange(0, data.shape[1] * hop_size, hop_size) / sr,
        np.fft.rfftfreq(dft_size, 1.0 / sr),
        np.log(np.abs(data)),
        cmap="magma",
    )

    ax.set_title(title)

    if label_axis:
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")

    return ax


def freqshow(
    w: np.ndarray,
    h: np.ndarray,
    sr: int,
    cf: int | list[int] | None = None,
    ax: mplaxes.Axes | None = None,
    title: str = "",
    hz_db: bool = True,
    label_axis: bool = True,
    limit_axis: bool = True,
) -> mplaxes.Axes:
    if ax is None:
        ax = plt.gca()

    if hz_db:
        ax.plot(w * sr / (2 * np.pi), 20 * np.log10(np.abs(h)))
    else:
        ax.plot(w, np.abs(h))

    if cf is None:
        cf = []
    elif isinstance(cf, int):
        cf = [cf]

    for c in cf:
        ax.axvline(c, color="red")

    ax.grid(which="both", axis="both")
    ax.set_title(title)

    if label_axis:
        ax.set_ylabel(f"Amplitude{'(dB)' if hz_db else ''}")
        ax.set_xlabel(f"Frequency{'(Hz)' if hz_db else ''}")

    if limit_axis:
        xlim, ylim = ((0, sr / 2), (-100, 50)) if hz_db else ((0, np.pi), (-2, 2))
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    return ax


def freqshows(
    wh: list[tuple[np.ndarray, np.ndarray]],
    sr: int | list[int],
    cf: int | list[int] | list[list[int]] | None = None,
    titles: list[str] = [],
    suptitle: str = "",
):
    n = len(wh)
    if isinstance(sr, int):
        sr = [sr] * n

    sharex_arg = "all" if len(sr) == 1 else "none"

    fig, axes = plt.subplots(n, sharex=sharex_arg, figsize=_calculate_figure_size(n, 1))

    if isinstance(axes, mplaxes.Axes):
        axes = np.array([axes])

    if cf is None:
        cf = [[] for _ in range(n)]
    elif isinstance(cf, int):
        cf = [cf] * n

    titles.extend([""] * (min(n, axes.size) - len(titles)))

    for ax, (w, h), s, c, title in zip(axes, wh, sr, cf, titles):
        freqshow(
            w,
            h,
            s,
            c,
            ax,
            title,
            label_axis=False,
        )

    fig.suptitle(suptitle)
    fig.supxlabel("Frequency (Hz)")
    fig.supylabel("Amplitude (dB)")
    fig.tight_layout()

    return fig, axes


def specshows(
    input_sounds: list[np.ndarray],
    sr: int | list[int],
    titles: list[str] = [],
    suptitle: str = "",
):
    n = len(input_sounds)
    share_axis_arg = (
        "all" if len({sound.shape for sound in input_sounds}) == 1 else "none"
    )

    if isinstance(sr, int):
        sr = [sr] * n

    nrows, ncols = max(1, np.ceil(n / 2).astype(int)), 1 if n <= 1 else 2
    fig, axes = plt.subplots(
        nrows,
        ncols,
        sharex=share_axis_arg,
        sharey=share_axis_arg,
        figsize=_calculate_figure_size(nrows, ncols),
    )

    titles.extend([""] * (n - len(titles)))

    for x, s, ax, t in zip(input_sounds, sr, axes.flatten(), titles):
        specshow(stft(x), sr=s, ax=ax, title=t, label_axis=False)

    fig.suptitle(suptitle)
    fig.supxlabel("Time (s)")
    fig.supylabel("Frequency (Hz)")
    fig.tight_layout()

    return fig, axes


def stemshow(
    x: np.ndarray,
    ax: mplaxes.Axes | None = None,
    title: str = "",
    label_axis=True,
) -> mplaxes.Axes:
    if ax is None:
        ax = plt.gca()

    ax.stem(x, markerfmt=".")
    ax.set_title(title)

    if label_axis:
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")

    return ax


def impulse(n: int) -> np.ndarray:
    x = np.zeros(n)
    x[0] = 1
    return x


def impulseshow(
    b: np.ndarray,
    a: np.ndarray | int,
    sr: int,
    ax: mplaxes.Axes | None = None,
    title: str = "",
    label_axis=True,
    playback=False,
) -> mplaxes.Axes:
    x = signal.lfilter(b, a, impulse(sr))[
        : 4 * max(b.size, a.size if isinstance(a, np.ndarray) else 1)
    ]
    assert isinstance(x, np.ndarray)
    stem = stemshow(x, ax, title, label_axis)

    if ax is None:
        plt.show()
    if playback:
        sound(x, sr, title)

    return stem


def impulseshows(
    ba: list[tuple[np.ndarray, np.ndarray | int]],
    sr: int | list[int],
    titles: list[str] = [],
    suptitle: str = "",
    label_axis=True,
    playback=False,
):
    n = len(ba)
    sharex_arg = "none"

    if isinstance(sr, int):
        sharex_arg = "all"
        sr = [sr] * n

    fig, axes = plt.subplots(n, sharex=sharex_arg, figsize=_calculate_figure_size(n))

    if isinstance(axes, mplaxes.Axes):
        axes = np.array([axes])

    titles.extend([""] * (min(n, axes.size) - len(titles)))

    for ax, (b, a), s, title in zip(axes, ba, sr, titles):
        impulseshow(b, a, s, ax, title, False, playback)

    if label_axis:
        fig.supxlabel("Samples")
        fig.supylabel("Amplitude")

    fig.suptitle(suptitle)
    fig.tight_layout()

    return fig, axes


def sounds(
    sounds: list[np.ndarray], sr: int | list[int], labels: list[str] = [], title=""
) -> None:
    if title:
        print(title)

    labels.extend([""] * (len(sounds) - len(labels)))

    if isinstance(sr, int):
        sr = [sr] * len(sounds)

    for x, s, l in zip(sounds, sr, labels):
        sound(x, sr=s, label=l)
