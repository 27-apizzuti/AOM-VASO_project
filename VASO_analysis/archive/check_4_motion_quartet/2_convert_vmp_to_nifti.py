"""
Created on Fri Jan 21 17:36:06 2022

    Create nifti unthresholded t-maps (BV GLM)

INPUT: .VMP
OUTPUT: 5D nifti for BOLD and VASO + 3D nifti for ROI (under BOLD flag)

NOTE:   VASO t-values changed sign.
        Maps oder in .vmp: 1) Horizontal, 2) Vertical 3) Diag45 4) Diag135 5) All Conditions

@author: apizz
"""
import os
import numpy as np
import bvbabel
from copy import copy
import nibabel as nb

STUDY_PATH = "D:\\hor_vert_cluster\\maps"
SUBJ = ["sub-02"]
CONDT = ['standard']
FUNC = ["BOLD"]

for su in SUBJ:

    for fu in FUNC:

        FILENAME_VMP = '{}_{}_hor_vert.vmp'.format(su, fu)

        # Read VMP
        IN_FILE = os.path.join(STUDY_PATH, FILENAME_VMP)
        header, data = bvbabel.vmp.read_vmp(IN_FILE)
        print(data.shape)
        n_maps = header['NrOfSubMaps']

        # Find indices inside ROI (binary mask)
        #vox_idx = data > 0

        # Create 4D matrix of significant t-values (into the ROI)
        nii_tmaps = np.zeros(data.shape[:])
        if fu == "VASO_interp_LN":
            data *= -1

        nii_tmaps = data
        FILENAME_NII = '{}_{}_hor_vert.nii.gz'.format(su, fu)

        # Save nifti t-maps
        outname = os.path.join(STUDY_PATH, FILENAME_NII)
        img = nb.Nifti1Image(nii_tmaps, affine=np.eye(4))
        nb.save(img, outname)
