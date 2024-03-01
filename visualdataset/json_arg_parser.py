import json
import sys
from pathlib import Path
from typing import Sequence, TypeVar, Type

from pydantic import BaseModel, ValidationError

from visualdataset.args_types import Matcher
from visualdataset.manifest import OptionsLink
from visualdataset.wellknown import FREESURFER_MATCHERS, FREESURFER_OPTIONS, MALPEM_MATCHERS, MALPEM_OPTIONS


EVERYTHING_MATCHER: Sequence[Matcher] = [Matcher(key='type', value='file', regex=r'\.(nii(\.gz)?)|(mgz)$')]
"""
a Matcher matching all supported file formats.
"""


def parse_args(input_dir: Path, mode: str, matchers: str | None, options: str | None
               ) -> tuple[Sequence[Matcher], Sequence[OptionsLink]]:
    mode = mode.lower()
    matchers_list = None
    options_list = []

    if 'freesurfer' in mode:
        matchers_list = FREESURFER_MATCHERS
        options_list = FREESURFER_OPTIONS
    if 'malpem' in mode:
        matchers_list = MALPEM_MATCHERS
        options_list = MALPEM_OPTIONS

    if matchers is not None:
        matchers_list = deserialize_list(file_or_string(input_dir, matchers), Matcher, '--matchers')
    if options is not None:
        options_list = deserialize_list(file_or_string(input_dir, options), OptionsLink, '--options')

    if matchers_list is None:
        matchers_list = EVERYTHING_MATCHER

    return matchers_list, options_list


_M = TypeVar('_M', bound=BaseModel)


def file_or_string(dir: Path, arg: str) -> str:
    path = dir / arg
    try:
        is_file = path.is_file()
    except OSError:  # in case file name is too long (it's probably the value!)
        is_file = False
    if is_file:
        return path.read_text()
    return arg


def deserialize_list(s: str, t: Type[_M], flag: str) -> Sequence[_M]:
    try:
        data = json.loads(s)
    except json.JSONDecodeError:
        print(f'Invalid value for {flag}: not JSON')
        sys.exit(1)
    if not isinstance(data, list):
        print(f'Invalid value for {flag}: not JSON list')
        sys.exit(1)
    try:
        return [t.model_validate(x, strict=True) for x in data]
    except ValidationError as e:
        print(f"Invalid value for {flag}:")
        print(e)
        sys.exit(1)
