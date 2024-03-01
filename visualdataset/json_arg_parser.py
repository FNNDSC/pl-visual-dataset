import json
import sys
from pathlib import Path
from typing import Sequence, TypeVar, Type

from pydantic import BaseModel, ValidationError

from visualdataset.args_types import Matcher
from visualdataset.manifest import OptionsLink
from visualdataset.wellknown import FREESURFER_MATCHERS, FREESURFER_OPTIONS, MALPEM_MATCHERS, MALPEM_OPTIONS


def parse_args(input_dir: Path, mode: str, matchers: str | None, options: str | None
               ) -> tuple[Sequence[Matcher], Sequence[OptionsLink]]:
    mode = mode.lower()
    if mode.startswith('freesurfer'):
        return FREESURFER_MATCHERS, FREESURFER_OPTIONS
    if mode.startswith('malpem'):
        return MALPEM_MATCHERS, MALPEM_OPTIONS
    if mode == 'file':
        matchers_str = '[]' if matchers is None else (input_dir / matchers).read_text()
        options_str = '[]' if options is None else (input_dir / options).read_text()
    elif mode == 'string':
        matchers_str = '[]' if matchers is None else matchers
        options_str = '[]' if options is None else options
    else:
        print(f'Unsupported option --mode={mode}')
        sys.exit(1)
    matchers_list = deserialize_list(matchers_str, Matcher, '--matchers')
    options_list = deserialize_list(options_str, OptionsLink, '--options')
    return matchers_list, options_list


_M = TypeVar('_M', bound=BaseModel)


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
