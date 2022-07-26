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

SUB = 'sub-02'
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
PATH_COL = os.path.join(STUDY_PATH, SUB, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'columns')
PATH_MAP = os.path.join(STUDY_PATH, SUB, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2', 'maps')
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Conv_Columns')
FUNC = ['BOLD', 'VASO']

col_range = np.arange(0, 1, 0.05)
sen_map_col = np.zeros([len(col_range), 2])
sp_map_col = np.zeros([len(col_range), 2])
err_sen_map_col = np.zeros([len(col_range), 2])
err_sp_map_col = np.zeros([len(col_range), 2])
vol_col = np.zeros([len(col_range), 2])

for ifu, fu in enumerate(FUNC):
    # File definitions
    FILE1 = "sub-02_leftMT_Sphere16radius_BOLD_FDR_{}_columns_full_depth_UVD_columns_mode_filter_window_count_ratio.nii.gz".format(fu)
    FILE2 = "sub-02_leftMT_Sphere16radius_{}_sensitivity_map_scaled_4.nii.gz".format(fu)
    FILE3 = "sub-02_leftMT_Sphere16radius_{}_specificity_map_scaled_4.nii.gz".format(fu)
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
        sen_map_col[i, ifu] = np.mean(sen_map[idx])
        sp_map_col[i, ifu] = np.mean(sp_map[idx])
        err_sen_map_col[i, ifu] = scipy.stats.sem(sen_map[idx], axis=0)
        err_sp_map_col[i, ifu] = scipy.stats.sem(sp_map[idx], axis=0)

        vol_col[i, ifu] = ((np.sum(idx) * (0.2 *0.2*0.2))/tot_vol) *100
# -------------------------------------------------------------
# Figure preparation
my_dpi = 200
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi),
            dpi=my_dpi)
x = np.arange(0, 1, 0.1)
axs[0].plot(col_range*100, sen_map_col[..., 0], color='black')
axs[0].plot(col_range*100, sen_map_col[..., 1], color='red')
axs[0].set_xticks(x*100)
axs[0].axvspan(65-0.5, 65+0.5, facecolor='gold', alpha=0.5)
# axs[0].fill_between(col_range*100, sen_map_col[..., 0]-err_sen_map_col[...,0], sen_map_col[..., 0]+err_sen_map_col[...,0],
#                     alpha=0.2, facecolor='black', antialiased=True)
axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
axs[0].set_xlabel("Columnarity index")
axs[0].set_ylabel("Sensitivity")

axs[1].plot(col_range*100, sp_map_col[..., 0], color='black')
axs[1].plot(col_range*100, sp_map_col[..., 1], color='red')
axs[1].axvspan(65-0.5, 65+0.5, facecolor='gold', alpha=0.5)
axs[1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axs[1].set_xticks(x*100)
axs[1].set_xlabel("Columnarity index")
axs[1].set_ylabel("Specificity")
fig_filename = "{}_Sen_Spec_BOLD_VASO_Columnarity.jpeg".format(SUB)
plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()
