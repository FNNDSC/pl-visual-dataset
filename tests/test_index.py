from pathlib import Path
import pytest
from pytest_unordered import unordered

from visualdataset.index_nifti_dir import index_nifti_dir
from tests.example_matchers import FETAL_ATLAS_MATCHERS
from visualdataset.manifest import VisualDatasetFile


def test_index_dir(tmp_path: Path):
    example_files = [
        'Age 36/serag.nii.gz',
        'Age 37/ali.nii.gz',
        'Age 37/ali_regional.nii.gz',
        'Age 37/ali_tissue.nii.gz',
    ]
    for example in example_files:
        p = tmp_path / example
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()

    actual = list(index_nifti_dir(tmp_path, FETAL_ATLAS_MATCHERS))
    expected = [
        VisualDatasetFile(
            path='Age 36/serag.nii.gz',
            tags={
                'age': '36',
                'author': 'Ahmed Serag et al.',
                'institution': 'Imperial College London',
                'type': 'T2 MRI'
            },
        ),
        VisualDatasetFile(
            path='Age 37/ali.nii.gz',
            tags={
                'age': '37',
                'author': 'Ali Gholipour et al., CRL',
                'institution': "Boston Children's Hospital",
                'type': 'T2 MRI'
            }
        ),
        VisualDatasetFile(
            path='Age 37/ali_regional.nii.gz',
            tags={
                'age': '37',
                'author': 'Ali Gholipour et al., CRL',
                'institution': "Boston Children's Hospital",
                'type': 'labels',
                'labels': 'parcellation'
            }
        ),
        VisualDatasetFile(
            path='Age 37/ali_tissue.nii.gz',
            tags={
                'age': '37',
                'author': 'Ali Gholipour et al., CRL',
                'institution': "Boston Children's Hospital",
                'type': 'labels',
                'labels': 'tissue'
            }
        ),
    ]
    assert actual == unordered(expected)
