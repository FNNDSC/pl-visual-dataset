import sys
from typing import Sequence

from pydantic import TypeAdapter

from visualdataset.args_types import Matcher


FETAL_ATLAS_MATCHERS: Sequence[Matcher] = [
    *(Matcher(key='age', value=str(age), regex=f'Age {age}/') for age in range(10, 40, 1)),

    Matcher(key='author', value='Ahmed Serag et al.', regex=r'/serag\.nii\.gz$'),
    Matcher(key='author', value="Ali Gholipour et al., CRL", regex=r'/ali.*\.nii\.gz$'),
    Matcher(key='author', value="Kiho Im et al., FNNDSC", regex=r'/kiho\.nii\.gz$'),

    Matcher(key='institution', value="Boston Children's Hospital", regex=r'/(kiho|ali).*\.nii\.gz$'),
    Matcher(key='institution', value="Imperial College London", regex=r'/serag\.nii\.gz$'),

    Matcher(key='type', value='mri', regex=r'/(ali|aliexp|kiho|serag)\.nii\.gz$'),
    Matcher(key='type', value='segmentation', regex=r'/(ali|aliexp)_.+\.nii\.gz$'),
]

if __name__ == '__main__':
    adapter = TypeAdapter(Sequence[Matcher])
    print(adapter.dump_json(FETAL_ATLAS_MATCHERS).decode('utf-8'))
