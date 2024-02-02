#!/usr/bin/env python
import json
import shutil
import sys
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path
from typing import Iterable, Sequence

from chris_plugin import chris_plugin
from pydantic import TypeAdapter, ConfigDict, ValidationError

from pubchrisvisual import DISPLAY_TITLE
from pubchrisvisual.types import NiivueVolumeOptions, ChrisViewerFileOptions

parser = ArgumentParser(description='Adds options for viewing one file of each subject using ChRIS_ui.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--order', type=str,
                    help='Order of preference for file names as a comma-separated list')
parser.add_argument('--options', type=str, default='{}',
                    help='Mapping of file names to default Niivue options as stringified JSON')
parser.add_argument('--readme', type=str,
                    help='README file content')

VISIBLE = NiivueVolumeOptions(opacity=1.0, colormap='gray')
INVISIBLE = NiivueVolumeOptions(opacity=0.0, colormap='gray')

_OPTIONS_MAPPING_ADAPTER = TypeAdapter(dict[str, ChrisViewerFileOptions])
_OPTIONS_ADAPTER = TypeAdapter(ChrisViewerFileOptions)


@chris_plugin(
    parser=parser,
    title='Single Volume ChRIS Visual Dataset',
    category='Utility',
    min_memory_limit='256Mi',
    min_cpu_limit='200m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    configs = deserialize_mapping(options.options)
    order = [name.strip() for name in ','.strip(options.order)]
    print(DISPLAY_TITLE, flush=True)
    shutil.copytree(inputdir, outputdir, dirs_exist_ok=True)
    for folder in folders(outputdir):
        files = [p for p in folder.glob('*') if p.is_file()]
        preferred = get_preferred_file(files, order)
        for file in files:
            base_config = VISIBLE if file is preferred else INVISIBLE
            config = (base_config | configs[file.name]) if file.name in configs else base_config
            if config is base_config:
                print(f"warning: no file name given by --options matches {file}")
            sidecar = file.with_suffix(file.suffix + '.chrisvisualdataset.volume.json')
            with sidecar.open('wb') as f:
                f.write(_OPTIONS_ADAPTER.dump_json(config))

    if options.readme is not None:
        (outputdir / 'README.txt').write_text(options.readme)

    (outputdir / '.chrisvisualdataset.root.json').write_text('{}')


def get_preferred_file(files: Sequence[Path], order: Sequence[str]) -> Path:
    for preferred_name in order:
        for file in files:
            if file.name == preferred_name:
                return file
    return files[0]


def folders(p: Path) -> Iterable[Path]:
    return filter(is_nonempty_dir, p.glob('*'))


def is_nonempty_dir(p: Path) -> bool:
    if not p.is_dir():
        return False
    return next(p.glob('*'), None) is not None


def is_nifti(p: Path) -> bool:
    return p.suffix == '.nii.gz'


def deserialize_mapping(x: str) -> dict[str, ChrisViewerFileOptions]:
    try:
        return _OPTIONS_MAPPING_ADAPTER.validate_json(x, strict=True)
    except ValidationError as e:
        print("Invalid value for --options")
        for error in e.errors():
            if 'url' in error:
                del error['url']
            print(json.dumps(error))
        sys.exit(1)


if __name__ == '__main__':
    main()
