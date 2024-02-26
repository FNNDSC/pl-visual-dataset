import pytest
from pytest_unordered import unordered

from visualdataset.manifest import OptionsLink, VisualDatasetFile
from visualdataset.options import ChrisViewerFileOptions, NiivueVolumeSettings
from visualdataset.validate import dict_is_subset, check_indexed_file_has_options


def test_check_indexed_file_has_options_works():
    options = [
        OptionsLink(
            match={'type': 'MRI'},
            options=ChrisViewerFileOptions(
                name='Magnetic Resonance Imaging',
                niivue_defaults=NiivueVolumeSettings(colormap='gray')
            )
        ),
        OptionsLink(
            match={'creator': 'me'},
            options=ChrisViewerFileOptions(author='Me, who is a person', website='https://example.com')
        )
    ]
    file = VisualDatasetFile(path='iamthe.path', tags={'type': 'MRI', 'creator': 'me'})
    assert check_indexed_file_has_options(file, options) == []


def test_check_indexed_file_has_options_warnings():
    options = [
        OptionsLink(
            match={'type': 'MRI'},
            options=ChrisViewerFileOptions(
                name='Magnetic Resonance Imaging',
                niivue_defaults=NiivueVolumeSettings(opacity=0.8)
            ),
        ),
        OptionsLink(
            match={'creator': 'me'},
            options=ChrisViewerFileOptions(
                name='Made by me',
                niivue_defaults=NiivueVolumeSettings(opacity=0.5)
            )
        ),
    ]
    file = VisualDatasetFile(path='iamthe.path', tags={'type': 'MRI', 'creator': 'me'})
    expected = [
        '`name` was defined 2 times for "iamthe.path"',
        '`niivue_defaults.opacity` was defined 2 times for "iamthe.path"'
    ]
    assert check_indexed_file_has_options(file, options) == unordered(expected)

    file = VisualDatasetFile(path='iamthe.path', tags={'type': 'unmatchable'})
    expected = ['`name` is unset for "iamthe.path"']
    assert check_indexed_file_has_options(file, options) == unordered(expected)


@pytest.mark.parametrize(
    'a, b, expected',
    [
        (
            {},
            {},
            True
        ),
        (
            {'a': 'b'},
            {'a': 'b'},
            True
        ),
        (
            {'a': 'b'},
            {'a': 'c'},
            False
        ),
        (
            {'a': 'b', 'c': 'd'},
            {'a': 'b', 'c': 'd', 'e': 'f'},
            True
        ),
        (
            {'a': 'b', 'c': 'd', 'e': 'f'},
            {'a': 'b', 'c': 'd'},
            False
        ),
    ]
)
def test_dict_is_subset(a: dict[str, str], b: dict[str, str], expected: bool):
    assert dict_is_subset(a, b) == expected
