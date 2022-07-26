"""
Created on Wed Jul 28 19:49:31 2021
    CV-AVG red voxels in the scatterplot
    Scatterplot (sub-plot): Specificity vs Sensitivity

INPUT: .npy dictionary of all subjects
OUTPUT: figures


@author: apizz
"""
import os
import matplotlib.pyplot as plt
import numpy as np


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']
tag = 'c_thr_4'

VASO_BOLD_MASK = True
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'testScatterPlot')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# ===========================Execute========================================


for roi in ROI_NAME:
    red_dots = None  # Just to initialize
    my_dpi = 96
    rows = len(FUNC)
    cols = len(SUBJ)
    fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

    for i, su in enumerate(SUBJ):
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'GLM', 'ROI')
        PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'cross_validation', 'Results')

        n_vox_avg_cv = []
        n_vox_avg = []

        for j, fu in enumerate(FUNC):

            # Get data
            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

            # AVG dictionary
            NPY_FILENAME = "{}_{}_meanRuns_{}_ROI_{}_{}{}_tuning_dict.npy".format(su, fu, CONDT[0], roi, tag, mask_suffix)

            tuning_dict = np.load(os.path.join(PATH_IN, NPY_FILENAME),
                                  allow_pickle=True).item()

            # CV-AVG final voxels
            NPY_CV_AVG = "{}_{}_{}_{}{}_cv_step2_dict.npy".format(su, fu, roi, tag, mask_suffix)


            cv_avg_dict = np.load(os.path.join(PATH_CV, NPY_CV_AVG),
                                  allow_pickle=True).item()

            # Find discarded voxels from the cluster thresholding
            temp = cv_avg_dict["idx_AVG_3D"] == True
            idx = cv_avg_dict["idx_cv_avg_c_thr"]
            CV_AVG_C_THR = idx[temp>0]
            #---------------------------------------------------
            red_dots = CV_AVG_C_THR
            n_vox_avg_cv = np.sum(CV_AVG_C_THR > 0)
            n_vox_avg = CV_AVG_C_THR.shape
            perc = 100 *n_vox_avg_cv / n_vox_avg[0]

            # Plotting
            axs[j, i].scatter(tuning_dict['Sensitivity'],
                              tuning_dict['Specificity'],
                              color='black',
                              alpha=0.2)

            axs[j, i].set_ylabel("Specificity (1-div)")
            axs[j, i].set_xlabel("Sensitivity (L2norm)")
            # axs[j, i].set_ylim([0, 1])
            # axs[j, i].set_xlim([0, 30])
            axs[j, i].grid("True")
            axs[j, i].set_title("{}, {}/{} ({}%)\n".format(su, n_vox_avg_cv, n_vox_avg[0], int(perc)))

            # x = (tuning_dict['Sensitivity'])[red_dots]
            # y = (tuning_dict['Specificity'])[red_dots]
            # axs[j, i].scatter(x, y, color='red', alpha=0.25)
            # --------------------------------------------------------------------
            # # VASO specific things
            # if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
            #     red_dots -= tuning_dict['Label']
            #     red_dots = red_dots == 0
            #     print("{}/{}".format(np.sum(red_dots), red_dots.size))
            #     x = (tuning_dict['Sensitivity'])[red_dots]
            #     y = (tuning_dict['Specificity'])[red_dots]
            #     axs[j, i].scatter(x, y, color='red', alpha=0.25)
            # else:  # BOLD first
            #     red_dots = tuning_dict['Label']

            # --------------------------------------------------------------------


    plt.suptitle("CV-AVG Voxel's Characterization {} \n\n\n".format(roi))
    fig_filename = "black_ACG_All_sbj_{}_CV_AVG_c_thresh_Voxel_Characterization_{}".format(roi, CONDT[0])
    fig.tight_layout()
    plt.savefig(os.path.join(PATH_OUT, fig_filename),
                bbox_inches='tight', dpi=my_dpi)
    plt.show()
