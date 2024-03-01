#!/usr/bin/env python
import os.path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path
from typing import Optional

from chris_plugin import chris_plugin
from pydantic import TypeAdapter

from visualdataset import DISPLAY_TITLE
from visualdataset.json_arg_parser import parse_args
from visualdataset.brain_dataset import brain_dataset

parser = ArgumentParser(description='Prepares a dataset for use with the ChRIS_ui '
                                    '"Visual Datasets" feature.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--mode', type=str, default='file', choices=['file', 'string', 'freesurfer-7.3.3', 'malpem-1.3'],
                    help='File matching and option selection mode. file=accept JSON files from '
                         '--matchers and --options. string=accept JSON strings from --matchers and --options. '
                         'freesurfer=built-in support for the FreeSurfer output files.')
parser.add_argument('--matchers', type=str,
                    help='Regular expressions used to assign tags to files')
parser.add_argument('--options', type=str,
                    help='Metadata to go with tag sets')
parser.add_argument('--first-run-files', type=str, default='[]',
                    help='List of files to show on first run, '
                         'as a stringified JSON list of paths relative to inputdir')
parser.add_argument('--first-run-tags', type=str, default='{}',
                    help='Tags to show on first run as a stringified JSON object')
parser.add_argument('--readme', type=str,
                    help='README file content')

_LIST_ADAPTER = TypeAdapter(list[str])
_DICT_ADAPTER = TypeAdapter(dict[str, str])


@chris_plugin(
    parser=parser,
    title='ChRIS Visual Dataset Indexer',
    category='Utility',
    min_memory_limit='1Gi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    matchers, tag_options = parse_args(inputdir, options.mode, options.matchers, options.options)
    first_run_files = _LIST_ADAPTER.validate_json(options.first_run_files)
    first_run_tags = _DICT_ADAPTER.validate_json(options.first_run_tags)

    if not first_run_files:
        if options.mode.lower().startswith('freesurfer'):
            first_run_files.extend(find_first_matching(inputdir, 'T1.mgz'))
        elif options.mode.lower().startswith('malpem'):
            first_run_files.extend(find_first_matching(inputdir, '*_N4_masked.nii.gz'))
            first_run_files.extend(find_first_matching(inputdir, '*_MALPEM.nii.gz'))

    print(DISPLAY_TITLE, flush=True)
    brain_dataset(inputdir, outputdir, matchers, tag_options, first_run_files, first_run_tags, options.readme)


def find_first_matching(input_dir: Path, glob: str) -> list[str]:
    matches = filter(os.path.isfile, input_dir.rglob(glob))
    rel = map(lambda p: p.relative_to(input_dir), matches)
    rel_as_str = map(str, rel)
    if some := next(rel_as_str, None):
        return [some]
    return []


if __name__ == '__main__':
    main()
