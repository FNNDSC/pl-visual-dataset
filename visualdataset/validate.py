from collections import Counter
from typing import Sequence, Mapping

from visualdataset.manifest import VisualDatasetFile, OptionsLink
from visualdataset.options import ChrisViewerFileOptions, NiivueVolumeSettings

IMPORTANT_KEYS = ('name', 'author', 'niivue_defaults.colormap')
"""
Keys of ``ChrisViewerFileOptions`` which are important. If a file lacks these options,
then warnings should be printed.
"""


def check_indexed_file_has_options(file: VisualDatasetFile, options: Sequence[OptionsLink]) -> Sequence[str]:
    """
    Validate that:

    1. No option is defined more than once
    2. Some important options are defined once
    """
    matched_options = [o.options for o in options if dict_is_subset(o.match, file.tags)]
    counts = _count_option_keys(matched_options)
    multiple = {k: v for k, v in counts.items() if v > 1}
    left_out = [k for k, v in counts.items() if v == 0 and k in IMPORTANT_KEYS]
    return ([f'`{k}` was defined {v} times for "{file.path}"' for k, v in multiple.items()]
            + [f'`{k}` is unset for "{file.path}"' for k in left_out])


def dict_is_subset(a: Mapping[str, str], b: Mapping[str, str]) -> bool:
    """
    :return: True if all key-value pairs in a are also in b
    """
    return all(k in b and b[k] == v for k, v in a.items())


def _count_option_keys(matched_options: Sequence[ChrisViewerFileOptions]):
    """
    Count the number of times each option key and each niivue_defaults setting is defined.
    """
    counter = _create_counter()
    for options in matched_options:
        for k in options.keys():
            if k == 'niivue_defaults':
                continue
            counter[k] += 1
        if 'niivue_defaults' in options:
            for k in options['niivue_defaults'].keys():
                counter[f'niivue_defaults.{k}'] += 1
    return counter


def _create_counter():
    options_keys = {k: 0 for k in ChrisViewerFileOptions.__annotations__.keys()}
    del options_keys['niivue_defaults']
    niivue_keys = {f'niivue_defaults.{k}': 0 for k in NiivueVolumeSettings.__annotations__.keys()}
    return Counter(**options_keys, **niivue_keys)
