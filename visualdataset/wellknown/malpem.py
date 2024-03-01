from typing import Sequence

from visualdataset.args_types import Matcher
from visualdataset.manifest import OptionsLink
from visualdataset.options import ChrisViewerFileOptions, NiivueVolumeSettings

MALPEM_MATCHERS: Sequence[Matcher] = [
    Matcher(key='type', value='T1 MRI', regex=r'.+_N4(_masked)?\.nii\.gz'),
    Matcher(key='type', value='labels', regex=r'.+_MALPEM(_tissues)?\.nii\.gz'),
    Matcher(key='name', value='Head', regex=r'.+_N4\.nii\.gz'),
    Matcher(key='name', value='Brain', regex=r'.+_N4_masked\.nii\.gz'),
    Matcher(key='name', value='MALP-EM tissue segmentation', regex=r'.+_MALPEM_tissues\.nii\.gz'),
    Matcher(key='name', value='MALP-EM structure segmentation', regex=r'.+_MALPEM\.nii\.gz'),
]

MALPEM_OPTIONS: Sequence[OptionsLink] = [
    OptionsLink(
        match={'type': 'T1 MRI'},
        options=ChrisViewerFileOptions(niivue_defaults=NiivueVolumeSettings(colormap='gray'))
    ),
    OptionsLink(
        match={'type': 'labels'},
        options=ChrisViewerFileOptions(
            citation=[
                'C. Ledig, R. A. Heckemann, A. Hammers, J. C. Lopez, V. F. J. Newcombe, A. Makropoulos, J. Loetjoenen, '
                'D. Menon and D. Rueckert, "Robust whole-brain segmentation: Application to traumatic brain injury", '
                'Medical Image Analysis, 21(1), pp. 40-58, 2015.'
            ]
        )
    ),
    OptionsLink(
        match={'name': 'Head'},
        options=ChrisViewerFileOptions(name='Head T1 MRI (corrected)')
    ),
    OptionsLink(
        match={'name': 'Brain'},
        options=ChrisViewerFileOptions(name='Extracted Brain')
    ),
    OptionsLink(
        match={'name': 'MALP-EM tissue segmentation'},
        options=ChrisViewerFileOptions(
            name='MALP-EM tissue segmentation',
            niivue_defaults=NiivueVolumeSettings(colormap='roi_i256', opacity=0.2, cal_min=0, cal_max=256)
        )
    ),
    OptionsLink(
        match={'name': 'MALP-EM structure segmentation'},
        options=ChrisViewerFileOptions(
            name='MALP-EM structure segmentation',
            niivue_defaults=NiivueVolumeSettings(colormapLabelFile='MALP-EM.v1.3.json', opacity=0.2)
        )
    ),
]
