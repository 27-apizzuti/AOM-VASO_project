"""
Created on Thu Mar  3 10:50:11 2022

@author: apizz
"""

import numpy as np
import os
import subprocess
import nibabel as nb

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
BINX = [532, 461, 426, 461, 568]
BINZ = [107, 103, 109, 103, 115]
FUNC = ['BOLD', 'VASO']

for itsbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'maps')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'maps')
    print('{}'.format(su))

    FILE1 = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_VASO_winner_map_scaled_4.nii.gz'.format(su))
    FILE2 = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_BOLD_winner_map_scaled_4.nii.gz'.format(su))

    output_name = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_consistent_winner_map.nii.gz'.format(su))

    # Get data
    nii1 = nb.load(FILE1)
    data1 = nii1.get_fdata()

    nii2 = nb.load(FILE2)
    data2 = nii2.get_fdata()

    # Compute columnar volume that is common between BOLD and VASO
    idx1 = data1 > 0
    idx2 = data2 > 0
    idx3 = data1 == data2

    idx = idx3 * idx1 * idx2

    # Save back nifti with consistent columns
    new_data = np.zeros(np.shape(data2))
    new_data[idx] = data1[idx]

    out = nb.Nifti1Image(new_data, header=nii1.header, affine=nii1.affine)
    nb.save(out, output_name)
