from pathlib import PurePath
from typing import Sequence, Mapping, Set, Self

from pydantic import BaseModel, ConfigDict

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
    tags: Mapping[str, Set[str] | Sequence[str]]
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

    def sort(self) -> Self:
        sorted_tags = {
            k: sorted(v)
            for k, v in sorted(self.tags.items())
        }
        sorted_files = sorted(self.files, key=_get_path)
        sorted_file_paths = [f.path for f in sorted_files]
        sorted_first_run_files = [
            sorted_file_paths.index(self.files[i].path)
            for i in self.first_run_files
        ]
        return self.model_copy(update={
            'tags': sorted_tags,
            'files': sorted_files,
            'first_run_files': sorted_first_run_files
        })


def _get_path(x: VisualDatasetFile) -> str:
    return str(x.path)
