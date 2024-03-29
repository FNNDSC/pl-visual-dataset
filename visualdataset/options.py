"""
"ChRIS visual dataset" defaults specification
"""

from typing import TypedDict, NotRequired, Sequence
from pydantic import ConfigDict, TypeAdapter, HttpUrl


class NiivueVolumeSettings(TypedDict):
    """
    Settings supported by Niivue for volumes.

    https://github.com/niivue/niivue-react/blob/d56dcd2b3f58ce854686e77963f3a7a89599765f/src/model.ts#L30-L76
    """
    opacity: NotRequired[float]
    colormap: NotRequired[str]
    colormapNegative: NotRequired[str]
    cal_min: NotRequired[float]
    cal_max: NotRequired[float]
    trustCalMinMax: NotRequired[bool]
    visible: NotRequired[bool]
    colorbarVisible: NotRequired[bool]

    colormapLabelFile: NotRequired[str]
    """
    File name containing JSON object to be used for the value of ``colormapLabel``, which
    sets the color map for a label-type volume (e.g. segmentation).
    
    ``colormapLabelFile`` can be relative to the input directory, or it may be a pre-installed file.
    It must be in the NiiVue JSON format.
    """

    __pydantic_config__ = ConfigDict(extra='forbid')


class ChrisViewerFileOptions(TypedDict):
    """
    Options supported by ChRIS_ui for files.
    """
    name: NotRequired[str]
    """
    Short, human-readable name of file (to be shown instead of the file name)
    """
    author: NotRequired[str]
    """
    Lab, institution, or person who is credited for this dataset
    """
    description: NotRequired[str]
    """
    Optional longer description of file. E.g. the description may contain credits, patient description...
    """
    citation: NotRequired[Sequence[str]]
    """
    Academic references for the dataset
    """
    website: NotRequired[HttpUrl]
    """
    Website for the dataset
    """
    niivue_defaults: NotRequired[NiivueVolumeSettings]
    """
    Default volume rendering options
    """

    __pydantic_config__ = ConfigDict(extra='forbid')
