import os
import numpy as np
import torch
import librosa

from tqdm import tqdm
from vocal_remover.lib import dataset, nets, spec_utils

N_FFT = 2048
HOP_LENGTH = 1024
BATCH_SIZE = 4
CROP_SIZE = 256
PRETRAINED_MODEL = "vocal_remover/models/baseline.pth"

print("loading model...", end=" ")
device = torch.device("cpu")
model = nets.CascadedNet(N_FFT, HOP_LENGTH, 32, 128, True)
model.load_state_dict(torch.load(PRETRAINED_MODEL, map_location="cpu"))
model.to(device)
print("done")


class Separator(object):
    def __init__(
        self, model, device=None, batchsize=1, cropsize=256, postprocess=False
    ) -> None:
        self.model = model
        self.offset = model.offset
        self.device = device
        self.batchsize = batchsize
        self.cropsize = cropsize
        self.postprocess = postprocess

    def _postprocess(self, X_spec, mask) -> tuple:
        if self.postprocess:
            mask_mag = np.abs(mask)
            mask_mag = spec_utils.merge_artifacts(mask_mag)
            mask = mask_mag * np.exp(1.0j * np.angle(mask))

        y_spec = X_spec * mask
        v_spec = X_spec - y_spec

        return y_spec, v_spec

    def _separate(self, X_spec_pad, roi_size) -> np.ndarray:
        X_dataset = []
        patches = (X_spec_pad.shape[2] - 2 * self.offset) // roi_size
        for i in range(patches):
            start = i * roi_size
            X_spec_crop = X_spec_pad[:, :, start : start + self.cropsize]
            X_dataset.append(X_spec_crop)

        X_dataset = np.asarray(X_dataset)

        self.model.eval()
        with torch.no_grad():
            mask_list = []
            # To reduce the overhead, dataloader is not used.
            for i in tqdm(range(0, patches, self.batchsize)):
                X_batch = X_dataset[i : i + self.batchsize]
                X_batch = torch.from_numpy(X_batch).to(self.device)

                mask = self.model.predict_mask(X_batch)

                mask = mask.detach().cpu().numpy()
                mask = np.concatenate(mask, axis=2)
                mask_list.append(mask)

            mask = np.concatenate(mask_list, axis=2)

        return mask

    def separate(self, X_spec) -> tuple:
        n_frame = X_spec.shape[2]
        pad_l, pad_r, roi_size = dataset.make_padding(
            n_frame, self.cropsize, self.offset
        )
        X_spec_pad = np.pad(X_spec, ((0, 0), (0, 0), (pad_l, pad_r)), mode="constant")
        X_spec_pad /= np.abs(X_spec).max()

        mask = self._separate(X_spec_pad, roi_size)
        mask = mask[:, :, :n_frame]

        y_spec, v_spec = self._postprocess(X_spec, mask)

        return y_spec, v_spec

    def separate_tta(self, X_spec):
        n_frame = X_spec.shape[2]
        pad_l, pad_r, roi_size = dataset.make_padding(
            n_frame, self.cropsize, self.offset
        )
        X_spec_pad = np.pad(X_spec, ((0, 0), (0, 0), (pad_l, pad_r)), mode="constant")
        X_spec_pad /= X_spec_pad.max()

        mask = self._separate(X_spec_pad, roi_size)

        pad_l += roi_size // 2
        pad_r += roi_size // 2
        X_spec_pad = np.pad(X_spec, ((0, 0), (0, 0), (pad_l, pad_r)), mode="constant")
        X_spec_pad /= X_spec_pad.max()

        mask_tta = self._separate(X_spec_pad, roi_size)
        mask_tta = mask_tta[:, :, roi_size // 2 :]
        mask = (mask[:, :, :n_frame] + mask_tta[:, :, :n_frame]) * 0.5

        y_spec, v_spec = self._postprocess(X_spec, mask)

        return y_spec, v_spec


SP = Separator(
    model=model,
    device=device,
    batchsize=BATCH_SIZE,
    cropsize=CROP_SIZE,
)


def remove_vocals(x: np.ndarray, tta: bool = True) -> np.ndarray:
    if x.ndim == 1:
        x = np.array([x, x])

    print(x.shape)

    print("stft of input x...", end=" ")
    X_spec = spec_utils.wave_to_spectrogram(x, HOP_LENGTH, N_FFT)
    print("done")

    y_spec, _ = SP.separate_tta(X_spec) if tta else SP.separate(X_spec)

    print("validating output directory...", end=" ")
    output_dir = "./"
    if output_dir != "":  # modifies output_dir if theres an arg specified
        output_dir = output_dir.rstrip("/") + "/"
        os.makedirs(output_dir, exist_ok=True)
    print("done")

    print("inverse stft of instruments...", end=" ")
    wave = spec_utils.spectrogram_to_wave(y_spec, hop_length=HOP_LENGTH)
    print("done")

    return wave.T
