import os.path
from pathlib import Path, PurePath
from typing import Iterator, Sequence

from visualdataset.args_types import Matcher
from visualdataset.manifest import VisualDatasetFile

_SUPPORTED_VOLUME_FILE_EXTENSIONS = ('.nii.gz', '.nii', '.mgz')
"""
File extensions supported by Niivue.

https://github.com/niivue/niivue?tab=readme-ov-file#supported-formats
"""


def index_brain_dir(input_dir: Path, matchers: Sequence[Matcher]) -> Iterator[VisualDatasetFile]:
    """
    Scan a directory for files matching the matchers.
    """
    brain_files = filter(is_volume_file, input_dir.rglob('*'))
    rel_paths = (p.relative_to(input_dir) for p in brain_files)
    matches = (match_file(p, matchers) for p in rel_paths)
    return filter(_has_tags, matches)


def is_volume_file(p: Path) -> bool:
    if not p.is_file():
        return False
    return any(map(p.name.endswith, _SUPPORTED_VOLUME_FILE_EXTENSIONS))


def match_file(path: PurePath, matchers: Sequence[Matcher]) -> VisualDatasetFile:
    tags = {
        matcher.key: matcher.value
        for matcher in matchers
        if matcher.re.search(str(path)) is not None
    }
    return VisualDatasetFile(path=PurePath(path), tags=tags)


def _has_tags(match: VisualDatasetFile) -> bool:
    return len(match.tags) > 0
