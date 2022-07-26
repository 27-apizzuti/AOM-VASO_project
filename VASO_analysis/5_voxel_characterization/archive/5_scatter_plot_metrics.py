"""
Created on Wed Jul 28 19:49:31 2021

    Scatterplot (sub-plot): Specificity vs Sensitivity (single-subject)

INPUT: .npy dictionary of all subjects
OUTPUT: figures

NOTES: Run separately for ROI (left, right) reference impliced in VMP filename

OPTIONS:
    VASO_BOLD_MASK=True BOLD-VOXELS will be used for VASO

@author: apizz
"""
import os
import matplotlib.pyplot as plt
import numpy as np


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
# SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
SUBJ = ['sub-02']
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ['leftMT_Sphere16radius']
tag = 'c_thr_0'
VASO_BOLD_MASK = False

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# ===========================Execute========================================

for roi in ROI_NAME:
    red_dots = None  # Just to initialize
    my_dpi = 96
    fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ)+1, figsize=(1920/my_dpi, 1080/my_dpi),
                        dpi=my_dpi)

    for i, su in enumerate(SUBJ):
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI')
        for j, fu in enumerate(FUNC):

            # Get data
            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

            NPY_FILENAME = "{}_{}_meanRuns_{}_ROI_{}_{}{}_tuning_dict.npy".format(su, fu, CONDT[0], roi, tag, mask_suffix)

            tuning_dict = np.load(os.path.join(PATH_IN, NPY_FILENAME),
                                  allow_pickle=True).item()

            # Plotting
            axs[j, i].scatter(tuning_dict['Sensitivity'],
                              tuning_dict['Specificity'],
                              color='black',
                              alpha=0.2)
            axs[j, i].set_ylabel("Specificity (1-div)")
            axs[j, i].set_xlabel("Sensitivity (L2norm)")
            axs[j, i].set_ylim([0, 1])
            axs[j, i].set_xlim([0, 30])
            axs[j, i].grid("True")
            axs[j, i].set_title("{} {}".format(su, fu))

            # --------------------------------------------------------------------
            # # VASO specific things
            # if fu == "VASO" and VASO_BOLD_MASK:
            #     red_dots -= tuning_dict['Label']
            #     red_dots = red_dots == 0
            #     print("{}/{}".format(np.sum(red_dots), red_dots.size))
            #     x = (tuning_dict['Sensitivity'])[red_dots]
            #     y = (tuning_dict['Specificity'])[red_dots]
            #     axs[j, i].scatter(x, y, color='red', alpha=0.25)
            # else:  # BOLD first
            #     red_dots = tuning_dict['Label']

            # --------------------------------------------------------------------


    plt.suptitle("Voxel Characterization {}{}\n\n".format(roi, mask_suffix))
    fig_filename = "All_sbj_{}_Voxel_Characterization_{}_{}{}".format(
        roi, tag, CONDT[0], mask_suffix)
    fig.tight_layout()
    # plt.savefig(os.path.join(PATH_OUT, fig_filename),
                # bbox_inches='tight', dpi=my_dpi)
    plt.show()
