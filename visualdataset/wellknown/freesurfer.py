"""
See https://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation
"""

from typing import Sequence

from visualdataset.args_types import Matcher
from visualdataset.manifest import OptionsLink
from visualdataset.options import ChrisViewerFileOptions, NiivueVolumeSettings

FREESURFER_MATCHERS: Sequence[Matcher] = [
    Matcher(key='type', value='T1 MRI', regex=r'mri/T1\.(mgz|nii|nii\.gz)$'),
    Matcher(key='name', value='T1 MRI', regex=r'mri/T1\.(mgz|nii|nii\.gz)$'),
    Matcher(key='type', value='T1 MRI', regex=r'mri/brainmask\.(mgz|nii|nii\.gz)$'),
    Matcher(key='name', value='brain', regex=r'mri/brainmask\.(mgz|nii|nii\.gz)$'),

    Matcher(key='type', value='labels', regex=r'mri/wmparc\.(mgz|nii|nii\.gz)$'),
    Matcher(key='labels', value='White Matter Parcellation', regex=r'mri/wmparc\.(mgz|nii|nii\.gz)$'),

    Matcher(key='type', value='labels', regex=r'mri/aparc\.a2009s\+aseg\.(mgz|nii|nii\.gz)$'),
    Matcher(key='labels', value='Destrieux Atlas Parcellation', regex=r'mri/aparc\.a2009s\+aseg\.(mgz|nii|nii\.gz)$'),

    Matcher(key='type', value='labels',
            regex=r'mri/aparc\.DKTatlas\+aseg(\.(orig|deep|deep\.withCC))?\.(mgz|nii|nii\.gz)$'),
    Matcher(key='labels', value='DKTatlas',
            regex=r'mri/aparc\.DKTatlas\+aseg(\.(orig|deep|deep\.withCC))?\.(mgz|nii|nii\.gz)$'),
    Matcher(key='program', value='FreeSurfer',
            regex=r'mri/aparc\.DKTatlas\+aseg\.(mgz|nii|nii\.gz)$'),
    Matcher(key='program', value='FastSurfer',
            regex=r'mri/aparc\.DKTatlas\+aseg\.deep(\.withCC)?\.(mgz|nii|nii\.gz)$'),
    Matcher(key='withCC', value='yes',
            regex=r'mri/aparc\.DKTatlas\+aseg\.deep\.withCC\.(mgz|nii|nii\.gz)$'),
    Matcher(key='withCC', value='no',
            regex=r'mri/aparc\.DKTatlas\+aseg\.deep\.(mgz|nii|nii\.gz)$'),
    Matcher(key='orig', value='yes',
            regex=r'mri/aparc\.DKTatlas\+aseg\.orig\.(mgz|nii|nii\.gz)$')
]

FREESURFER_OPTIONS: Sequence[OptionsLink] = [
    OptionsLink(
        match={'type': 'T1 MRI'},
        options=ChrisViewerFileOptions(niivue_defaults=NiivueVolumeSettings(colormap='gray'))
    ),
    OptionsLink(
        match={'name': 'T1 MRI'},
        options=ChrisViewerFileOptions(name='T1 MRI')
    ),
    OptionsLink(
        match={'name': 'brain'},
        options=ChrisViewerFileOptions(name='Extracted brain (skull-stripped)')
    ),
    OptionsLink(
        match={'type': 'labels'},
        options=ChrisViewerFileOptions(
            niivue_defaults=NiivueVolumeSettings(colormapLabelFile='FreeSurferColorLUT.v7.3.3.json')
        )
    ),
    OptionsLink(
        match={'labels': 'White Matter Parcellation'},
        options=ChrisViewerFileOptions(name='White Matter Parcellation')
    ),
    OptionsLink(
        match={'labels': 'Destrieux Atlas Parcellation'},
        options=ChrisViewerFileOptions(name='Destrieux Atlas Parcellation')
    ),
    OptionsLink(
        match={'labels': 'DKTatlas', 'program': 'FreeSurfer'},
        options=ChrisViewerFileOptions(name='Desikan-Killiany Atlas')
    ),
    OptionsLink(
        match={'labels': 'DKTatlas', 'program': 'FastSurfer', 'withCC': 'yes'},
        options=ChrisViewerFileOptions(name='Desikan-Killiany Atlas (FastSurfer, with corpus callosum)')
    ),
    OptionsLink(
        match={'labels': 'DKTatlas', 'program': 'FastSurfer', 'withCC': 'no'},
        options=ChrisViewerFileOptions(name='Desikan-Killiany Atlas (FastSurfer)')
    ),
    OptionsLink(
        match={'labels': 'DKTatlas', 'orig': 'yes'},
        options=ChrisViewerFileOptions(name='Desikan-Killiany Atlas (original)')
    ),
]
