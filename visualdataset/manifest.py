from pathlib import PurePath
from pydantic import BaseModel, ConfigDict
from typing import Sequence, FrozenSet, Tuple, Mapping, Optional, Set

from visualdataset.options import ChrisViewerFileOptions


class VisualDatasetFile(BaseModel):
    """
    Index data about a file of a "visual dataset".
    """
    path: PurePath
    """
    Path of file relative to the plugin instance's output directory.
    """
    tags: Mapping[str, str]
    """
    Metadata as key-value pairs which identify the file.
    """
    has_sidecar: bool = False
    """
    Whether or not the file has a corresponding `.chrisvisualdataset.volume.json` sidecar file.
    """

    __pydantic_config__ = ConfigDict(extra='forbid')


class OptionsLink(BaseModel):
    """
    An association between some options and a set of tags.
    """
    match: Mapping[str, str]
    options: ChrisViewerFileOptions


class VisualDatasetManifest(BaseModel):
    """
    A list of all the files and metadata of a "visual dataset".
    """
    tags: Mapping[str, Set[str]]
    """
    All known tags and all known values for each tag.
    """
    files: Sequence[VisualDatasetFile]
    """
    Files in this dataset.
    """
    options: Sequence[OptionsLink]
    """
    Options for files.
    """
    first_run_files: Sequence[int]
    """
    Index numbers into ``files`` for which files to show when the viewer is first opened.
    """

    __pydantic_config__ = ConfigDict(extra='forbid')
