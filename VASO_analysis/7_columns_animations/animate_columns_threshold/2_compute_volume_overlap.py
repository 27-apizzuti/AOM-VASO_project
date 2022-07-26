"""
Created on Thu Mar  3 10:50:11 2022
BOLD VASO spatial consistency

@author: apizz
"""

import numpy as np
import os
import subprocess
import nibabel as nb
import matplotlib.pyplot as plt

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02','sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
BINX = [532, 461, 426, 461, 568]
BINZ = [107, 103, 109, 103, 115]

FUNC = ['BOLD', 'VASO']
threshold = np.arange(25, 100, 1)

consistency = np.zeros([len(SUBJ), 75])
my_dpi = 200

for itsbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'columns_threshold')
    PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Conv_Columns')


    for i, itThr in enumerate(threshold):

        FILE1 = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_BOLD_winner_map_{}_COL_MASK.nii.gz'.format(su, itThr))
        FILE2 = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_VASO_winner_map_{}_COL_MASK.nii.gz'.format(su, itThr))

        output_name = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_consistent_winner_map_{}_COL_MASK.nii.gz'.format(su, itThr))
        print('For {}, consistency at {}'.format(su, itThr))
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

        # Reference: OR opearation between BOLD and VASO columns for each C.I. threshold
        temp = np.logical_or(idx1, idx2)
        ntot = np.sum(temp)

        consistency[itsbj, i] = np.sum(idx)
        consistency[itsbj, i] = (consistency[itsbj, i]/ntot) * 100

# Make plot
fig, axs = plt.subplots(dpi=my_dpi)
axs.plot(threshold, np.mean(consistency, axis=0), 'k-')
axs.set_xlabel("Columnarity index")
axs.set_ylabel("% Consistent voxels")
plt.grid()
plt.savefig(os.path.join(PATH_OUT, "Summary_consistent_columns.png"), bbox_inches='tight', dpi=my_dpi)
plt.savefig(os.path.join(PATH_OUT, "Summary_consistent_columns.svg"), bbox_inches='tight', dpi=my_dpi)
