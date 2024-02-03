import sys
from pathlib import Path
from typing import Sequence, Optional, Mapping, Set

from tqdm import tqdm

from visualdataset.args_types import Matcher
from visualdataset.index_nifti_dir import index_nifti_dir
from visualdataset.manifest import VisualDatasetFile, OptionsLink, VisualDatasetManifest
from visualdataset.nifti_sidecar import create_sidecar


def nifti_dataset(
        input_dir: Path,
        output_dir: Path,
        matchers: Sequence[Matcher],
        options: Sequence[OptionsLink],
        first_run_files: Sequence[str],
        readme: Optional[str]
):
    with tqdm(desc='Scanning input directory...'):
        index = [i.model_copy(update={'has_sidecar': True}) for i in index_nifti_dir(input_dir, matchers)]

    if not index:
        print(f'Error: nothing matched for: {[m.regex for m in matchers]}')
        sys.exit(1)

    first_run_index_nums = find_first_run_files(input_dir, index, first_run_files)

    with tqdm(index, desc='Writing outputs') as pbar:
        for file in pbar:
            output_path = output_dir / file.path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sidecar_path = output_path.with_suffix(output_path.suffix + '.chrisvisualdataset.volume.json')
            create_sidecar(input_dir / file.path, sidecar_path)

    manifest = VisualDatasetManifest(
        tags=aggregate_tags(index),
        files=index,
        options=options,
        first_run_files=first_run_index_nums
    )

    manifest_path = output_dir / '.chrisvisualdataset.tagmanifest.json'
    manifest_path.write_text(manifest.model_dump_json())

    if readme is not None:
        readme_path = output_dir / 'README.txt'
        readme_path.write_text(readme)


def aggregate_tags(index: Sequence[VisualDatasetFile]) -> Mapping[str, Set[str]]:
    """
    Get all tag and all of their possible values.
    """
    tags = {}
    for file in index:
        for key, value in file.tags.items():
            if key not in tags:
                tags[key] = set()
            tags[key].add(value)
    return tags


def find_first_run_files(
        input_dir: Path,
        index: Sequence[VisualDatasetFile],
        first_run_files: Sequence[str]
) -> Sequence[int]:
    """
    Find all elements of ``first_run_files`` as paths in ``index``, then return a list of their array index numbers.
    """
    first_run_index_nums = []
    indexed_paths = [str(file.path) for file in index]
    for file in first_run_files:
        try:
            first_run_index_nums.append(indexed_paths.index(file))
        except ValueError:
            print(f'File was not matched: {file}')
            sys.exit(1)
    return first_run_index_nums
