"""
Created on Mon Oct  4 11:54:56 2021
Group Result
Create Tuning Curves Averaged across subjects (AVG or CV);
Load all the subjects at once and make a unique plot
NB: CV = True -> cross validated set of voxels
@author: apizz

"""

import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ['leftMT_Sphere16radius']
tag = 'c_thr_4'
VASO_BOLD_MASK = True
CV = True


PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'WinnerMaps')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

for roi in ROI_NAME:

    # Initialize output variables
    tuning = np.zeros([2, 4, 4, 2])   # contrast, class, class, mean, std
    NrOfVox = np.zeros([2, 4])        # contrast, class, perc (respect to the tot numb of voxels -> summing all sbj)
    n_vox = np.zeros([2, 3])          # constrast, tot.num, (min, max)

    for iterContr, fu in enumerate(FUNC):

        # Get data
        mask_suffix = ""
        if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
            mask_suffix = "_BOLDMASK"

        t_values_allSbj = [[], [], [], []]
        n_vox_allSbj = np.zeros([len(SUBJ), 4, 2])

        for iterSbj, su in enumerate(SUBJ):
            PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                           'vaso_analysis', CONDT[0], 'GLM', 'ROI')
            NPY_FILENAME = "{}_{}_meanRuns_{}_ROI_{}_{}{}_tuning_dict.npy".format(su, fu, CONDT[0], roi, tag, mask_suffix)

            tuning_dict = np.load(os.path.join(PATH_IN, NPY_FILENAME),
                                      allow_pickle=True).item()

            if CV:
                suffix = 'CV_AVG_'
                PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'cross_validation', 'Results')
                # CV-AVG final voxels
                NPY_CV_AVG = "{}_{}_{}_{}{}_cv_step2_dict.npy".format(su, fu, roi, tag, mask_suffix)


                cv_avg_dict = np.load(os.path.join(PATH_CV, NPY_CV_AVG),
                                      allow_pickle=True).item()

                # Find discarded voxels from the cluster thresholding
                temp = cv_avg_dict["idx_AVG_3D"] == True
                idx = cv_avg_dict["idx_cv_avg_c_thr"]
                CV_AVG_C_THR = idx[temp>0]                         # // boolean same lenght of AVG 1D
                # Extract voxel tvalue for each class and compute tuning
                vox_tvalue = tuning_dict['TValues'] * CV_AVG_C_THR[..., None]
                vox_label = tuning_dict['Label'] * CV_AVG_C_THR
            else:
                suffix = ""

                # Extract voxel tvalue for each class and compute tuning
                vox_tvalue = tuning_dict['TValues']
                vox_label = tuning_dict['Label']
            for k, j in enumerate(range(1, 5)):
                vox_data = vox_tvalue[vox_label == j, :]
                t_values_allSbj[k].extend(vox_data)
                n_vox_allSbj[iterSbj, k, 0] = vox_data.shape[0]
                n_vox_allSbj[iterSbj, k, 1] = vox_data.shape[0] / vox_tvalue.shape[0] * 100

        n = np.sum(np.sum(n_vox_allSbj[..., 0], axis=1))
        for it in range(0, 4):
            x = np.asarray(t_values_allSbj[it])
            tuning[iterContr, it, :, 0] = np.mean(x, axis=0)
            tuning[iterContr, it, :, 1] = scipy.stats.sem(x, axis=0)
            NrOfVox[iterContr, it] = x.shape[0] / n * 100

        n_vox[iterContr, :] = [n, np.min(np.sum(n_vox_allSbj[..., 0], axis=1)), np.max(np.sum(n_vox_allSbj[..., 0], axis=1))]

# %% Plotting
    my_dpi = 96
    x = np.array([1, 2, 3, 4])
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    contrast = ["Horizontal", "Vertical", "Diagonal 45°-225°", "Diagonal 135°-315°"]

    for k in range(0, 4):
        axs[k].errorbar(x, tuning[0, k, :, 0], tuning[0, k, :, 1], color='black', label='BOLD')
        axs[k].errorbar(x, tuning[1, k, :, 0], tuning[1, k, :, 1], color='red', label='VASO')

        axs[k].axvspan(x[k]-0.5, x[k]+0.5, facecolor='#2ca02c', alpha=0.5)
        axs[k].set_title("{}".format(contrast[k]))
        axs[k].set_xticks(x)
        axs[k].set_ylim([0, 5.5])
        axs[k].set_ylabel("T-value")
        axs[k].set_xlabel("Conditions")
        axs[k].legend();

    # text_counts = "|BOLD: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f} ({:.0f}, {:.0f})|\n|VASO: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f}, ({:.0f}, {:.0f})|".format(NrOfVox[0, 0],
    #                                                               NrOfVox[0, 1],
    #                                                               NrOfVox[0, 2],
    #                                                               NrOfVox[0, 3],
    #                                                               n_vox[0, 0], n_vox[0, 1], n_vox[0, 2],
    #                                                               NrOfVox[1, 0],
    #                                                               NrOfVox[1, 1],
    #                                                               NrOfVox[1, 2],
    #                                                               NrOfVox[1, 3],
    #                                                               n_vox[1, 0], n_vox[1, 1], n_vox[1, 2])

    # plt.suptitle('Group results: Tuning curves {}{}\n\n{}'.format(mask_suffix, roi, text_counts))
    # plt.suptitle('Group results: Tuning curves {}{}\n\n'.format(mask_suffix, roi))
    fig_filename = "{}Group_results_{}_Tuning_Curves_{}_{}_{}_range_0_5.svg".format(suffix, mask_suffix, roi, CONDT[0], tag)
    plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
    plt.show()
