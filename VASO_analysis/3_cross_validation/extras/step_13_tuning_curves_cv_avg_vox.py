"""
Created on Wed Jul 28 14:51:03 2021
    Tuning Curves (single subject)

INPUT: .npy dictionary of all subjects
OUTPUT: figures

OPTIONS:
    VASO_BOLD_MASK=True BOLD-VOXELS will be used for VASO

@author: apizz
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["rightMT_Sphere16radius", "leftMT_Sphere16radius"]
tag = 'c_thr_4'
VASO_BOLD_MASK = True

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'WinnerMaps')
if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

# ===========================Execute========================================
for roi in ROI_NAME:
    for su in SUBJ:
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'GLM', 'ROI')
        PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'cross_validation', 'Results')


        # Initialize output variables
        tuning = np.zeros([2, 4, 4, 2])
        NrOfVox = np.zeros([2, 4, 2])
        n_vox = np.zeros(2)

        for iterfu, fu in enumerate(FUNC):
            print(fu)
            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

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
            CV_AVG_C_THR = idx[temp>0]                         # // boolean same lenght of AVG 1D
            #---------------------------------------------------

            # Extract voxel tvalue for each class and compute tuning
            vox_tvalue = tuning_dict['TValues'] * CV_AVG_C_THR[..., None]
            vox_label = tuning_dict['Label'] * CV_AVG_C_THR

            n_vox[iterfu] = np.sum(CV_AVG_C_THR > 0)
            for i, j in enumerate(range(1, 5)):
                vox_data = vox_tvalue[vox_label == j, :]
                tuning[iterfu, i, :, 0] = np.mean(vox_data, axis=0)
                tuning[iterfu, i, :, 1] = scipy.stats.sem(vox_data, axis=0)        # standard error
                NrOfVox[iterfu, i, 0] = vox_data.shape[0]
                NrOfVox[iterfu, i, 1] = vox_data.shape[0] / n_vox[iterfu] * 100

        # %% Plotting
        my_dpi = 96
        x = np.array([1, 2, 3, 4])
        fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
        contrast = ["Horizontal", "Vertical", "Diag45", "Diag135"]

        for k in range(0, 4):
            axs[k].errorbar(x, tuning[0, k, :, 0], tuning[0, k, :, 1], color='black', label='BOLD')
            axs[k].errorbar(x, tuning[1, k, :, 0], tuning[1, k, :, 1], color='red', label='VASO')

            axs[k].axvspan(x[k]-0.5, x[k]+0.5, facecolor='#2ca02c', alpha=0.5)
            axs[k].set_title("Tuning for {}".format(contrast[k]))
            axs[k].set_xticks(x)
            axs[k].set_ylim([0, 6])
            axs[k].set_ylabel("T-value")
            axs[k].set_xlabel("Conditions")
            axs[k].legend();
        # fig_filename = 'allsubject_smooth_{}_{}_vmin_{}_vmax_{}.png'.format(smt_suffix, rest, my_vmin[smt], my_vmax[smt])

        text_counts = "|BOLD: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f}|\n|VASO: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f}|".format(NrOfVox[0, 0, 1],
                                                                     NrOfVox[0, 1, 1],
                                                                     NrOfVox[0, 2, 1],
                                                                     NrOfVox[0, 3, 1],
                                                                     n_vox[0],
                                                                     NrOfVox[1, 0, 1],
                                                                     NrOfVox[1, 1, 1],
                                                                     NrOfVox[1, 2, 1],
                                                                     NrOfVox[1, 3, 1],
                                                                     n_vox[1])
        plt.suptitle('CV AVG Tuning curves {}{}\n\n{}'.format(mask_suffix, roi, text_counts))
        fig_filename = "CV_AVG_{}_Tuning_Curves_{}_{}_{}{}".format(su, roi, CONDT[0], tag, mask_suffix)
        plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
        plt.show()
