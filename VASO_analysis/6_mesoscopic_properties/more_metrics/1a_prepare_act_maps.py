"""
Created on Tue Jan 18 12:40:57 2022

Investigating draining vein effect.

Make a 5D nifti with unthresholded activation maps for a specific ROI.
Maps already upsampled of factor 4.

Maps order:
    Vertical, Horiz, Diag45, Diag135, All axes of motion

@author: apizz
"""

import os
import numpy as np
import nibabel as nb

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI_NAME = 'leftMT_Sphere16radius'
MAPS_NAME = ['Horizontal', 'Vertical','Diag45', 'Diag135', 'allTask']

for su in SUBJ:

    PATH_ACT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'ACTIVATION', 'scaled_4')

    ROI = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2', '{}_{}_scaled_4.nii.gz'.format(su, ROI_NAME))

    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2')

    if not os.path.exists(PATH_OUT):
        print("Creating folder")
        os.mkdir(PATH_OUT)

    nii = nb.load(ROI)
    vox_roi = nii.get_fdata()  # ROI
    dims = np.shape(vox_roi)

    # Create 5D nifti
    new_nifti = np.zeros(dims + (5,))

    for fu in FUNC:
        print("Merging act. maps for {}, {}, {}".format(su, fu, ROI_NAME))
        for it, a_map in enumerate(MAPS_NAME):

            FILE = 'scaled_4_act_{}_{}.nii'.format(a_map, fu)
            nii = nb.load(os.path.join(PATH_ACT, FILE))
            vox_map = nii.get_fdata()  # map

            temp = vox_map * vox_roi  # mask with ROI
            new_nifti[..., it] = temp

        # Export 5D nifti
        outname = os.path.join(PATH_OUT, "{}_{}_{}_5psc_scaled_4_unthreshold.nii.gz".format(su, fu, ROI_NAME))
        img = nb.Nifti1Image(new_nifti, affine=nii.affine)
        nb.save(img, outname)
