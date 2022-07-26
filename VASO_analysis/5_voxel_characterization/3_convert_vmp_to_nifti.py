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

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["leftMT_Sphere16radius"]

for su in SUBJ:
    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'GLM', 'ROI')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'masks_maps')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
        os.mkdir(os.path.join(PATH_OUT, 'res_pt8'))

    for roi in ROI_NAME:
        for fu in FUNC:
            print("Processing {} {} ROI {}".format(fu, su, roi))

            FILENAME_VMP = '{}_{}_meanRuns_{}_ROI_{}.vmp'.format(su, fu, CONDT[0], roi)

            # Read VMP
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data = bvbabel.vmp.read_vmp(IN_FILE)
            print(data.shape)
            n_maps = header['NrOfSubMaps']

            # Find indices inside ROI (binary mask)
            vox_idx = data[..., 5] > 0

            # Create 4D matrix of significant t-values (into the ROI)
            nii_tmaps = np.zeros(data.shape[0:3] + (5,))
            if fu == "VASO_interp_LN":
                data *= -1
                filename = "{}_VASO_{}_tmaps.nii.gz".format(su, roi)
            else:
                filename = "{}_BOLD_{}_tmaps.nii.gz".format(su, roi)
                # Save nifti ROI
                outname = os.path.join(PATH_OUT, 'res_pt8', "{}_{}.nii.gz".format(su, roi))
                img = nb.Nifti1Image(data[..., 5], affine=np.eye(4))
                nb.save(img, outname)

            for iterCond in range(0, 5):
                nii_tmaps[vox_idx, iterCond] = data[vox_idx, iterCond]

            # Save nifti t-maps
            outname = os.path.join(PATH_OUT, 'res_pt8', filename)
            img = nb.Nifti1Image(nii_tmaps, affine=np.eye(4))
            nb.save(img, outname)
