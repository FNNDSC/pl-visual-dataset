import os.path
from pathlib import Path, PurePath
from typing import Iterator, Sequence

from visualdataset.args_types import Matcher
from visualdataset.manifest import VisualDatasetFile


def index_nifti_dir(input_dir: Path, matchers: Sequence[Matcher]) -> Iterator[VisualDatasetFile]:
    """
    Scan a directory for files matching the matchers.
    """
    nifti_files = filter(os.path.isfile, input_dir.rglob('*.nii.gz', case_sensitive=False))
    rel_paths = (p.relative_to(input_dir) for p in nifti_files)
    matches = (match_file(p, matchers) for p in rel_paths)
    return filter(_has_tags, matches)


def match_file(path: PurePath, matchers: Sequence[Matcher]) -> VisualDatasetFile:
    tags = {
        matcher.key: matcher.value
        for matcher in matchers
        if matcher.re.search(str(path)) is not None
    }
    return VisualDatasetFile(path=PurePath(path), tags=tags)


def _has_tags(match: VisualDatasetFile) -> bool:
    return len(match.tags) > 0
