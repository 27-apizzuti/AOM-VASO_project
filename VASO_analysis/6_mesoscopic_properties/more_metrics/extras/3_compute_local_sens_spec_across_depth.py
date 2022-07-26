"""
Created on Tue Jan 18 15:44:39 2022

Prepare depth-dependent in house sens. and spec. and EPI for vessel detection (BOLD_mean.nii)

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI_NAME = 'leftMT_Sphere16radius'
MAPS_NAME = ['Vertical', 'Horizontal', 'Diag45', 'Diag135', 'allTask']
n_lay = 21

for su in SUBJ:

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2')

    PATH_LAY = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4')

    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'EPI_vessels')

    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    # Import metric file
    FILE = os.path.join(PATH_LAY, '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    nii = nb.load(FILE)
    metric = nii.get_fdata()

    # Obtain 21 equidist layers
    metric = metric.flatten()
    idx_vox = metric > 0

    # FILE2: BOLDMask
    FILE2 = os.path.join(PATH_IN, 'masks', "{}_{}_BOLD_FDR_mask_scaled_4.nii.gz".format(su, ROI_NAME))
    nii2 = nb.load(FILE2)
    vox_mask = nii2.get_fdata()
    vox_mask = vox_mask.flatten()
    idx = (vox_mask > 0) * (idx_vox)



    for i, fu in enumerate(FUNC):
        # Figure preparation
        my_dpi = 96
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi),
                        dpi=my_dpi)

        # Import sensitivity map
        FILE = os.path.join(PATH_IN, 'maps', "{}_{}_{}_sensitivity_map_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        sens_map = nii.get_fdata()
        sens_map = sens_map.flatten()

        # Import specificity map
        FILE = os.path.join(PATH_IN, 'maps', "{}_{}_{}_specificity_map_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        spec_map = nii.get_fdata()
        spec_map = spec_map.flatten()

        # Import BOLD_mean
        FILE = os.path.join(PATH_IN, "BOLD_mean_{}_scaled_4.nii.gz".format(ROI_NAME))
        nii = nb.load(FILE)
        epi_map = nii.get_fdata()
        epi_map = epi_map.flatten()

        # Scatterplot
        x = metric[idx]
        axs[0, 0].scatter(x, sens_map[idx], color='black', alpha=0.2)
        axs[0, 0].set_ylabel("Sensitivity (L2norm)")
        # axs[0, 0].set_ylim([0, 30])
        axs[0, 0].grid("True")

        axs[0, 1].scatter(x, spec_map[idx], color='black',
                              alpha=0.2)
        axs[0, 1].set_ylabel("Specificity (1-div)")
        # axs[0, 1].set_ylim([0, 1])
        axs[0, 1].grid("True")

        axs[1, 0].scatter(x, epi_map[idx], color='black', alpha=0.2)
        axs[1, 0].set_ylabel("EPI intensity")
        # axs[1, 0].set_xlim([0, 30])
        axs[1, 0].grid("True")

        axs[1, 1].scatter(x, epi_map[idx], color='black', alpha=0.2)
        axs[1, 1].set_ylabel("EPI intensity")
        # axs[1, 0].set_xlim([0, 30])
        axs[1, 1].grid("True")

        # Save figure
        plt.suptitle("EPI_vein Detection for {}, {}".format(su, fu))
        fig_filename = "EPI_vein_detection_{}_{}".format(su, fu)
        fig.tight_layout()
        plt.savefig(os.path.join(PATH_OUT, fig_filename),
                bbox_inches='tight', dpi=my_dpi)
        plt.show()
