from typing import Sequence

from pydantic import TypeAdapter

from visualdataset.args_types import Matcher

FETAL_ATLAS_MATCHERS: Sequence[Matcher] = [
    *(Matcher(key='age', value=str(age), regex=f'Age {age}/') for age in range(10, 40, 1)),

    Matcher(key='author', value='Ahmed Serag et al.', regex=r'/serag.*\.nii\.gz$'),
    Matcher(key='author', value='Ali Gholipour et al., CRL', regex=r'/ali.*\.nii\.gz$'),
    Matcher(key='author', value='Kiho Im et al., FNNDSC', regex=r'/kiho.*\.nii\.gz$'),

    Matcher(key='institution', value="Boston Children's Hospital", regex=r'/(kiho|ali).*\.nii\.gz$'),
    Matcher(key='institution', value="Imperial College London", regex=r'/serag.*\.nii\.gz$'),

    Matcher(key='type', value='T2 MRI', regex=r'_template\.nii\.gz$'),
    Matcher(key='type', value='ventricles', regex=r'_ventricles\.nii\.gz$'),
    Matcher(key='type', value='labels', regex=r'_(tissue|regional)\.nii\.gz$'),
    Matcher(key='labels', value='tissue', regex=r'/(ali|aliexp)_tissue\.nii\.gz$'),
    Matcher(key='labels', value='parcellation', regex=r'/(ali|aliexp)_regional\.nii\.gz$'),
]

if __name__ == '__main__':
    adapter = TypeAdapter(Sequence[Matcher])
    print(adapter.dump_json(FETAL_ATLAS_MATCHERS).decode('utf-8'))
