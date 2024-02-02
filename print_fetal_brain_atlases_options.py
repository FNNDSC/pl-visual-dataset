#!/usr/bin/env python
"""
Notes:

```
pubone --order 'kiho.nii.gz,serag.nii.gz,ali.nii.gz,aliexp.nii.gz' \
       --options "$(./print_atlas_options.py)" \
       --readme "Fetal brain T2 MRI atlas datasets curated by the Fetal-Neonatal Neuroimaging Developmental Science Center. https://www.fnndsc.org/" \
       incoming/ outgoing/
```
"""
import json
import sys

from pubchrisvisual.types import ChrisViewerFileOptions, NiivueVolumeOptions


MRI_OPTIONS = NiivueVolumeOptions(colormap="gray", colorbarVisible=False)
LABEL_OPTIONS = NiivueVolumeOptions(colormap="roi_i256", colorbarVisible=False)

CRL_MRI_OPTIONS = ChrisViewerFileOptions(
    name="T2 MRI",
    author="CRL (Ali Gholipour et al.)",
    description="Fetal T2 atlas developed by the Computational Radiology Laboratory of "
                   "Boston Children's Hospital, Harvard Medical School.",
    website="http://crl.med.harvard.edu/research/fetal_brain_atlas/",
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
    options=MRI_OPTIONS
)

CRL_REGIONAL_OPTIONS = CRL_MRI_OPTIONS | ChrisViewerFileOptions(
    name="Regional cortex parcellation",
    description="Regional cortex parcellation of the CRL fetal brain atlas.",
    options=LABEL_OPTIONS
)

CRL_TISSUE_OPTIONS = CRL_MRI_OPTIONS | ChrisViewerFileOptions(
    name="Tissue segmentation (\"Olympic edition\")",
    description="Tissue segmentation of the CRL fetal brain atlas.",
    options=LABEL_OPTIONS
)

KIHO_MRI_OPTIONS = ChrisViewerFileOptions(
    name="T2 MRI",
    author="FNNDSC (Kiho Im et al)",
    description="Fetal T2 atlas developed by the MRI group of the Fetal-Neonatal Neuroimaging Developmental Science "
                "Center at the Boston Children's Hospital",
    website="https://research.childrenshospital.org/neuroim/",
    options=MRI_OPTIONS
)

SERAG_MRI_OPTIONS = ChrisViewerFileOptions(
    name="T2 MRI",
    author="Imperial College London (Serag et al.)",
    description="Fetal T2 atlas developed at the Imperial College London.",
    website="https://brain-development.org/brain-atlases/fetal-brain-atlases/fetal-brain-atlas-serag/",
    options=MRI_OPTIONS
)

FILENAME_MAPPING: dict[str, ChrisViewerFileOptions] = {
    "kiho.nii.gz": KIHO_MRI_OPTIONS,
    "serag.nii.gz": SERAG_MRI_OPTIONS,
    "ali.nii.gz": CRL_MRI_OPTIONS,
    "aliexp.nii.gz": CRL_MRI_OPTIONS,
    "ali_tissue.nii.gz": CRL_TISSUE_OPTIONS,
    "aliexp_tissue.nii.gz": CRL_TISSUE_OPTIONS,
    "ali_regional.nii.gz": CRL_REGIONAL_OPTIONS,
    "aliexp_regional.nii.gz": CRL_REGIONAL_OPTIONS
}

if __name__ == "__main__":
    json.dump(FILENAME_MAPPING, sys.stdout)
