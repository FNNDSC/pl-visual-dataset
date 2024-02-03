from pathlib import Path

import numpy as np
import nibabel as nib
from pydantic import TypeAdapter

from visualdataset.options import NiivueVolumeSettings

_SETTINGS_ADAPTER = TypeAdapter(NiivueVolumeSettings)


def create_sidecar(img: Path, output: Path):
    cal_min, cal_max = get_range(img)
    settings = NiivueVolumeSettings(cal_min=cal_min, cal_max=cal_max)
    output.write_bytes(_SETTINGS_ADAPTER.dump_json(settings))


def get_range(img: Path):
    vol = nib.load(img)
    data = vol.get_fdata()
    cal_min = np.min(data)
    cal_max = np.max(data)
    return cal_min, cal_max
