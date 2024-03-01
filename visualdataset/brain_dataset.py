import shutil
import sys
from pathlib import Path
from typing import Sequence, Optional, Mapping, Set, Iterator
import importlib.resources

from tqdm import tqdm

from visualdataset.args_types import Matcher
from visualdataset.index_brain_dir import index_brain_dir
from visualdataset.manifest import VisualDatasetFile, OptionsLink, VisualDatasetManifest
from visualdataset.volume_sidecar import create_sidecar
from visualdataset.validate import check_indexed_file_has_options, dict_is_subset


def brain_dataset(
        input_dir: Path,
        output_dir: Path,
        matchers: Sequence[Matcher],
        options: Sequence[OptionsLink],
        first_run_files: Sequence[str],
        first_run_tags: Mapping[str, str],
        readme: Optional[str]
):
    with tqdm(desc='Scanning input directory...'):
        index = [i.model_copy(update={'has_sidecar': True}) for i in index_brain_dir(input_dir, matchers)]

    if not index:
        print(f'Error: nothing matched for: {[m.regex for m in matchers]}')
        sys.exit(1)

    for file in index:
        for warning_message in check_indexed_file_has_options(file, options):
            print(warning_message)

    first_run_index_nums = find_first_run_files(input_dir, index, first_run_files)
    first_run_file_index = (index[i] for i in first_run_index_nums)
    first_run_known_tags = (file.tags for file in first_run_file_index)
    if not all(dict_is_subset(first_run_tags, tags) for tags in first_run_known_tags):
        print('Error: value for --first-run-tags is not a subset of every matched tag '
              'for the files of --first-run-files')
        sys.exit(1)

    copy_colormaplabel_files(options, input_dir, output_dir)

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
    manifest_path.write_text(manifest.sort().model_dump_json())

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


def copy_colormaplabel_files(options: Sequence[OptionsLink], input_dir: Path, output_dir: Path):
    for file in colormaplabel_files_of(options):
        shutil.copy(resolve_colormaplabel(file, input_dir), output_dir / file)


def resolve_colormaplabel(file: str, input_dir: Path) -> Path:
    """
    If ``file`` is found in ``input_dir``, return its path.
    Else, look for the file in this package's files.
    """
    path = input_dir / file
    if path.is_file():
        return path
    trav = importlib.resources.files(__package__).joinpath('colormaps', file)
    if trav.is_file():
        with importlib.resources.as_file(trav) as trav_path:
            return trav_path
    print(f'colormapLabel not found: "{file}"')
    sys.exit(1)


def colormaplabel_files_of(options: Sequence[OptionsLink]) -> Iterator[str]:
    return filter(lambda x: x is not None, map(colormaplabel_of, options))


def colormaplabel_of(option: OptionsLink) -> Optional[str]:
    return option.options.get('niivue_defaults', {}).get('colormapLabelFile', None)
