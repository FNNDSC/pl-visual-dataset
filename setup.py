from setuptools import setup
import re

_version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")

def get_version(rel_path: str) -> str:
    """
    Searches for the ``__version__ = `` line in a source code file.

    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    """
    with open(rel_path, 'r') as f:
        matches = map(_version_re.search, f)
        filtered = filter(lambda m: m is not None, matches)
        version = next(filtered, None)
        if version is None:
            raise RuntimeError(f'Could not find __version__ in {rel_path}')
        return version.group(0)


setup(
    name='chrisvisualdataset',
    version=get_version('visualdataset/__init__.py'),
    description='Prepare the outputs of a feed for the "visual datasets" feature of ChRIS_ui.',
    author='FNNDSC',
    author_email='dev@babymri.org',
    url='https://github.com/FNNDSC/pl-visual-dataset',
    packages=['visualdataset'],
    package_data={
        'visualdataset': ['colormaps/*']
    },
    install_requires=['chris_plugin'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'visualdataset = visualdataset.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=8.0',
            'pytest-unordered~=0.5.2'
        ]
    }
)
