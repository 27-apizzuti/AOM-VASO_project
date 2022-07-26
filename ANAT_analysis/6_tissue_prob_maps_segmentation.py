"""
Created on Frid May 21 2021

Apply gaussian smoothing on tissue probability maps

@author: apizz
"""

import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter

# Define input
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-04']
PATH_SEG = os.path.join(STUDY_PATH, SUBJ[0], 'derivatives', 'anat', 'segmentation_4')

FILE1 = nb.load(os.path.join(PATH_SEG, SUBJ[0] + '_scaled_4_pve_0.nii.gz'))    # CSF
FILE2 = nb.load(os.path.join(PATH_SEG, SUBJ[0] + '_scaled_4_pve_1.nii.gz'))    # GM
FILE3 = nb.load(os.path.join(PATH_SEG, SUBJ[0] + '_scaled_4_pve_2.nii.gz'))    # WM
FILE4 = nb.load(os.path.join(PATH_SEG, SUBJ[0] + '_scaled_4_seg.nii.gz'))

# To Set as Input Parameters for filter
sig = 1
w_CSF = 0.05
w_GM = 2
w_WM = 1

# Extract the data matrix
data_CSF = FILE1.get_fdata()
data_GM = FILE2.get_fdata()
data_WM = FILE3.get_fdata()
data_SEG = FILE4.get_fdata()
dim = data_CSF.shape

# Apply gaussian filter
data_CSF = gaussian_filter(data_CSF, sigma=sig)
data_GM = gaussian_filter(data_GM, sigma=sig)
data_WM = gaussian_filter(data_WM, sigma=sig)

# Output matrix
# 1 CSF, 2 GM, 3 WM
temp = np.zeros(dim + (3,))
# Apply weights
temp[..., 0] = data_CSF * w_CSF
temp[..., 1] = data_GM * w_GM
temp[..., 2] = data_WM * w_WM

maxind = np.argmax(temp, axis=3)
data_winner = maxind + 1
data_winner[data_SEG == 0 ] = 0

FILE4 = nb.Nifti1Image(data_winner, affine=FILE4.affine, header=FILE4.header)
out_name = SUBJ[0] + '_scaled_4_seg_wCSF_' + str(w_CSF) + '_wGM_' + str(w_GM) + '_wWM_'+ str(w_WM) + '_sigma_' + str(sig)
out_name = out_name.replace('.', 'pt')
nb.save(FILE4, os.path.join(PATH_SEG, out_name + '.nii.gz'))
