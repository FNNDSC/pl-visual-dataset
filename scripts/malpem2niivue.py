import itertools
import json
from pathlib import Path
from typing import Iterator


def main():
    here = Path(__file__).parent
    nmm_info = here / 'data' / 'nmm_info.csv'
    roi_i256 = here / 'data' / 'roi_i256.json'
    output = here.parent / 'visualdataset' / 'colormaps' / 'MALP-EM.v1.3.json'

    with roi_i256.open('r') as f:
        cmap = json.load(f)

    labels = itertools.chain(iter_nmm_labels(nmm_info), itertools.repeat('NA'))
    cmap['labels'] = [label for _i, label in zip(cmap['I'], labels)]

    with output.open('w') as f:
        json.dump(cmap, f)


def iter_nmm_labels(p: Path) -> Iterator[str]:
    with p.open('r') as f:
        for line in f:
            _i, _abbreviation, name, _side = line.split(',')
            yield name


if __name__ == '__main__':
    main()
