import json
import sys
from pathlib import Path
from typing import Sequence, TypeVar, Type

from pydantic import BaseModel, ValidationError

from visualdataset.args_types import Matcher
from visualdataset.manifest import OptionsLink


def parse_args(matchers: str | None, options: str | None, input_dir: Path | None,
               ) -> tuple[Sequence[Matcher], Sequence[OptionsLink]]:
    if input_dir:
        matchers_str = '[]' if matchers is None else (input_dir / matchers).read_text()
        options_str = '[]' if options is None else (input_dir / options).read_text()
    else:
        matchers_str = '[]' if matchers is None else matchers
        options_str = '[]' if options is None else options
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
