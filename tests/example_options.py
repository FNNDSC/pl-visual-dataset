from typing import Sequence

from pydantic import TypeAdapter

from visualdataset.manifest import OptionsLink
from visualdataset.options import ChrisViewerFileOptions, NiivueVolumeSettings

FETAL_ATLAS_OPTIONS: Sequence[OptionsLink] = [
    OptionsLink(
        match={'author': 'Ali Gholipour et al., CRL'},
        options=ChrisViewerFileOptions(
            author='Ali Gholipour et al., CRL',
            website='http://crl.med.harvard.edu/research/fetal_brain_atlas/',
            citation=[
                "A Gholipour, CK Rollins, C Velasco-Annis, A Ouaalam, A Akhondi-Asl, O Afacan, C Ortinau, S Clancy, "
                "C Limperopoulos, E Yang, JA Estroff, and SK Warfield. A normative spatiotemporal MRI atlas of the "
                "fetal brain for automatic segmentation and analysis of early brain growth, Scientific Reports 7, "
                "Article number: 476 (2017). http://www.nature.com/articles/s41598-017-00525-w",
                "A Gholipour, C Limperopoulos, S Clancy, C Clouchoux, A Akhondi-Asl, J A Estroff, and S K Warfield. "
                "Construction of a Deformable Spatiotemporal MRI Atlas of the Fetal Brain: Evaluation of Similarity "
                "Metrics and Deformation Models. MICCAI 2014.",
                "S Khan, L Vasung, B Marami, CK Rollins, O Afacan, C Ortinau, E Yang, SK Warfield, and A Gholipour. "
                "Fetal Brain Growth Portrayed by a Spatiotemporal Diffusion Tensor MRI Atlas Computed From In Utero "
                "Images. NeuroImage 2018. https://doi.org/10.1016/j.neuroimage.2018.08.030"
            ],
        )
    ),
    OptionsLink(
        match={'author': 'Ahmed Serag et al.'},
        options=ChrisViewerFileOptions(
            author='Ahmed Serag et al.',
            website='https://brain-development.org/brain-atlases/fetal-brain-atlases/fetal-brain-atlas-serag/',
            citation=[
                'A. Serag, P. Aljabar, G. Ball, S.J. Counsell, J.P. Boardman, M.A. Rutherford, A.D. Edwards, '
                'J.V. Hajnal, D. Rueckert. “Construction of a consistent high-definition spatio-temporal atlas '
                'of the developing brain using adaptive kernel regression”. NeuroImage, 59 (3), 2255-65, 2012. '
                'http://dx.doi.org/10.1016/j.neuroimage.2011.09.062',
                'A. Serag, V. Kyriakopoulou, P. Aljabar, S.J. Counsell, J.P. Boardman, M.A. Rutherford, '
                'A.D. Edwards, J.V. Hajnal, D. Rueckert. “A Multi-channel 4D Probabilistic Atlas of the '
                'Developing Brain: Application to Fetuses and Neonates”. Special Issue of the Annals of '
                'the British Machine Vision Association, 2012.'
            ]
        )
    ),
    OptionsLink(
        match={'author': 'Kiho Im et al., FNNDSC'},
        options=ChrisViewerFileOptions(
            author='Kiho Im et al., FNNDSC',
            website='https://research.childrenshospital.org/neuroim/',
        )
    ),
    OptionsLink(
        match={'type': 'T2 MRI'},
        options=ChrisViewerFileOptions(
            name='T2 MRI',
            niivue_defaults=NiivueVolumeSettings(colormap='gray')
        )
    ),
    OptionsLink(
        match={'type': 'ventricles'},
        options=ChrisViewerFileOptions(
            name='Ventricles',
            niivue_defaults=NiivueVolumeSettings(colormap='red')
        )
    ),
    OptionsLink(
        match={'author': 'Ali Gholipour et al., CRL', 'labels': 'tissue'},
        options=ChrisViewerFileOptions(name='Tissue segmentation ("Olympic edition")')
    ),
    OptionsLink(
        match={'author': 'Ali Gholipour et al., CRL', 'labels': 'parcellation'},
        options=ChrisViewerFileOptions(name='Regional cortex parcellation of the CRL fetal brain atlas.')
    ),
    OptionsLink(
        match={'author': 'Ali Gholipour et al., CRL', 'type': 'labels'},
        options=ChrisViewerFileOptions(
            niivue_defaults=NiivueVolumeSettings(colormapLabelFile='CRLAtlasLUT.json')
        )
    ),
]

if __name__ == '__main__':
    adapter = TypeAdapter(Sequence[OptionsLink])
    print(adapter.dump_json(FETAL_ATLAS_OPTIONS).decode('utf-8'))
