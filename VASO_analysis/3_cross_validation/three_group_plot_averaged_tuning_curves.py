"""
Created on Mon Oct  4 11:54:56 2021

Create Tuning Curves Averaged across subjects;
Load all the subjects at once and make a unique plot

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
    tuning = np.zeros([4, 4, 4, 2])   # 2comm * contrast, class, class, mean, std
    NrOfVox = np.zeros([4, 4])        # 4contrast, class (respect to the tot numb of voxels -> summing all sbj)
    n_vox = np.zeros(4)          # constrast, tot.num, (min, max)

    # Loading groups indices
    PATH_IN = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')
    NPY = "Group_idices_BOLD_VASO_COMM_{}.npy".format(roi)
    group_dict = np.load(os.path.join(PATH_IN, NPY),
                                      allow_pickle=True).item()

    for iterContr, fu in enumerate(FUNC):


        # Get data
        mask_suffix = ""
        if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
            mask_suffix = "_BOLDMASK"

        t_values_allSbj_contr = [[], [], [], []]
        t_values_allSbj_best = [[], [], [], []]

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

                # Contrast-specific voxels
                if iterContr == 0:
                    idx_contr = group_dict["BOLD_vox"][iterSbj]
                else:
                    idx_contr = group_dict["VASO_vox"][iterSbj]

                idx_comm = group_dict["COMM_vox"][iterSbj]

                n_orig = np.sum(cv_avg_dict["idx_cv_avg_c_thr"] > 0)
                n_contr = np.sum(idx_contr > 0)
                n_comm = np.sum(idx_comm > 0)

                print("For {}, orig. # vox: {} = contr_vox {} + comm_vox {} = {}".format(su, n_orig, n_contr, n_comm, (n_contr + n_comm)))


                # Find discarded voxels from the cluster thresholding
                temp = cv_avg_dict["idx_AVG_3D"] == True
                idx = cv_avg_dict["idx_cv_avg_c_thr"] * idx_contr
                CV_AVG_C_THR = idx[temp>0]                         # // boolean same lenght of AVG 1D

                # Best voxels
                idx_best = cv_avg_dict["idx_cv_avg_c_thr"] * idx_comm
                best_CV_AVG_C_THR = idx_best[temp>0]                         # // boolean same lenght of AVG 1D

                # Extract voxel tvalue for each class and compute tuning
                vox_tvalue_contr = tuning_dict['TValues'] * CV_AVG_C_THR[..., None]
                vox_label_contr = tuning_dict['Label'] * CV_AVG_C_THR

                vox_tvalue_best = tuning_dict['TValues'] * best_CV_AVG_C_THR[..., None]
                vox_label_best = tuning_dict['Label'] * best_CV_AVG_C_THR

                print("For {}, orig. # vox: {} = contr_vox {} + comm_vox {} = {}".format(su, n_orig, np.sum(vox_label_contr > 0), np.sum(vox_label_best > 0), (np.sum(vox_label_contr > 0) + np.sum(vox_label_best > 0))))


            for k, j in enumerate(range(1, 5)):
                vox_data_contr = vox_tvalue_contr[vox_label_contr == j, :]

                t_values_allSbj_contr[k].extend(vox_data_contr)

                vox_data_best = vox_tvalue_best[vox_label_best == j, :]
                t_values_allSbj_best[k].extend(vox_data_best)

        for it in range(0, 4):
            x = np.asarray(t_values_allSbj_contr[it])
            y = np.asarray(t_values_allSbj_best[it])
            tuning[iterContr, it, :, 0] = np.mean(x, axis=0)
            tuning[iterContr, it, :, 1] = scipy.stats.sem(x, axis=0)

            tuning[iterContr+2, it, :, 0] = np.mean(y, axis=0)
            tuning[iterContr+2, it, :, 1] = scipy.stats.sem(y, axis=0)

            NrOfVox[iterContr, it] = x.shape[0]
            NrOfVox[iterContr+2, it] = y.shape[0]
            print("For {}, {}, Tuning curves contrast: {}, common: {}".format(su, fu, tuning[iterContr, it, :, 0], tuning[iterContr+2, it, :, 0]))

# %% Plotting
    my_dpi = 96
    x = np.array([1, 2, 3, 4])
    fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    contrast = ["Horizontal", "Vertical", "Diag45", "Diag135"]

    for k in range(0, 4):
        axs[k].errorbar(x, tuning[0, k, :, 0], tuning[0, k, :, 1], color='black', label='BOLD (#vox: {})'.format(int(NrOfVox[0, k])))
        axs[k].errorbar(x, tuning[1, k, :, 0], tuning[1, k, :, 1], color='red', label='VASO (#vox: {})'.format(int(NrOfVox[1, k])))

        axs[k].errorbar(x, tuning[2, k, :, 0], tuning[2, k, :, 1], color='grey', label='Ref. BOLD (#vox: {})'.format(int(NrOfVox[2, k])))
        axs[k].errorbar(x, tuning[3, k, :, 0], tuning[3, k, :, 1], color='pink', label='Ref. VASO (#vox: {})'.format(int(NrOfVox[3, k])))

        axs[k].axvspan(x[k]-0.5, x[k]+0.5, facecolor='#2ca02c', alpha=0.5)
        axs[k].set_title("Tuning for {}".format(contrast[k]))
        axs[k].set_xticks(x)
        axs[k].set_ylim([-1, 6])
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
    fig_filename = "{}_Group_results_Tuning_Curves_with_BESTvox".format(roi)
    plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
    plt.show()
