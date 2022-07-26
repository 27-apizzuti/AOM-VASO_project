"""
Created on Wed Apr 27 12:22:50 2022
Sensitivity and Specificity characterize cortical columms

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
# STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Conv_Columns')
FUNC = ['BOLD', 'VASO']
MASK = 'BOLD_FDR'

col_range = np.arange(0.20, 1, 0.05)  # columnarity index range

# Initialize output
sen_map_col = np.zeros([len(SUBJ), len(col_range), 2])
sp_map_col = np.zeros([len(SUBJ), len(col_range), 2])
err_sen_map_col = np.zeros([len(SUBJ), len(col_range), 2])
err_sp_map_col = np.zeros([len(SUBJ), len(col_range), 2])
vol_col = np.zeros([len(SUBJ), len(col_range), 2])

for isu, su in enumerate(SUBJ):
    print("Processing {}".format(su))
    PATH_COL = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'columns')
    PATH_MAP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'maps')

    for ifu, fu in enumerate(FUNC):
        # File definitions
        FILE1 = "{}_leftMT_Sphere16radius_{}_{}_columns_full_depth_UVD_columns_mode_filter_window_count_ratio.nii.gz".format(su, MASK, fu)
        FILE2 = "{}_leftMT_Sphere16radius_{}_sensitivity_map_scaled_4.nii.gz".format(su, fu)
        FILE3 = "{}_leftMT_Sphere16radius_{}_specificity_map_scaled_4.nii.gz".format(su, fu)
        # Loading
        nii1 = nb.load(os.path.join(PATH_COL, FILE1))
        col_map = nii1.get_fdata()

        nii2 = nb.load(os.path.join(PATH_MAP, FILE2))
        sen_map = nii2.get_fdata()

        nii3 = nb.load(os.path.join(PATH_MAP, FILE3))
        sp_map = nii3.get_fdata()

        # ------------------------------------------
        for i, icol in enumerate(col_range):
            idx = col_map > icol
            if i == 0:
                tot_vol = np.sum(idx) * (0.2 *0.2*0.2)
            sen_map_col[isu, i, ifu] = np.mean(sen_map[idx])
            sp_map_col[isu, i, ifu] = np.mean(sp_map[idx])
            err_sen_map_col[isu, i, ifu] = scipy.stats.sem(sen_map[idx], axis=0)
            err_sp_map_col[isu, i, ifu] = scipy.stats.sem(sp_map[idx], axis=0)

            vol_col[isu, i, ifu] = ((np.sum(idx) * (0.2 *0.2*0.2))/tot_vol) *100
# -------------------------------------------------------------
# Figure preparation

# Group result
my_dpi = 200
fig, axs = plt.subplots(nrows=1, ncols=1)

axs.plot(col_range*100, np.mean(sp_map_col[:, :, 0], axis=0), color='blue')
axs.plot(col_range*100, np.mean(sp_map_col[:, :, 1], axis=0), color='red')
axs.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axs.set_xlabel("Columnarity index")
axs.set_ylabel("Specificity")
axs.grid()
fig_filename = "GroupSbj_Specificity_BOLD_VASO_Columnarity.jpeg"
fig_filename = "GroupSbj_Specificity_BOLD_VASO_Columnarity.svg"

plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()


my_dpi = 200
fig, axs = plt.subplots(nrows=1, ncols=1)
axs.plot(col_range*100, np.mean(sen_map_col[:, :, 0], axis=0), color='blue')
axs.plot(col_range*100, np.mean(sen_map_col[:, :, 1], axis=0), color='red')
axs.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axs.set_xlabel("Columnarity index")
axs.set_ylabel("Sensitivity")
axs.grid()

fig_filename = "GroupSbj_Senitivity_BOLD_VASO_Columnarity.jpeg"
fig_filename = "GroupSbj_Senitivity_BOLD_VASO_Columnarity.svg"

plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()
