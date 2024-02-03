#!/usr/bin/env python
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path

from chris_plugin import chris_plugin
from pydantic import TypeAdapter

from visualdataset import DISPLAY_TITLE
from visualdataset.json_arg_parser import parse_args
from visualdataset.nifti_dataset import nifti_dataset
from visualdataset.options import ChrisViewerFileOptions

parser = ArgumentParser(description='Prepares a dataset for use with the ChRIS_ui '
                                    '"Visual Datasets" feature.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--matchers', type=str, required=True,
                    help='Regular expressions used to assign tags to files')
parser.add_argument('--options', type=str,
                    help='Metadata to go with tag sets')
parser.add_argument('-s', '--string-args', action='store_true',
                    help='Interpret --matchers and --options as data instead of paths')
parser.add_argument('--first-run-files', type=str,
                    help='List of files to show on first run, '
                         'as a stringified JSON list of paths relative to inputdir')
parser.add_argument('--readme', type=str,
                    help='README file content')

_LIST_ADAPTER = TypeAdapter(list[str])


@chris_plugin(
    parser=parser,
    title='Single Volume ChRIS Visual Dataset',
    category='Utility',
    min_memory_limit='1Gi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    matchers, tag_options = parse_args(options.matchers, options.options,
                                       None if options.string_args else inputdir)
    first_run_files = [] if options.first_run_files is None else _LIST_ADAPTER.validate_json(options.first_run_files)
    print(DISPLAY_TITLE, flush=True)
    nifti_dataset(inputdir, outputdir, matchers, tag_options, first_run_files, options.readme)


if __name__ == '__main__':
    main()
