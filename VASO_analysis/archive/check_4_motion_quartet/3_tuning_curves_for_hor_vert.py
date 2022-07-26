"""
Created on Wed Jul 28 14:51:03 2021
    Tuning Curves (subject-specfic)

INPUT: niftis of all subjects
OUTPUT: figures

@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
N_SUB = len(SUBJ)
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
MASK = ["BOLD_FDR_mask", "BOLD_FDR_mask"]
# MASK = ""
ROI_NAME = "leftMT_Sphere16radius"
N_CONTR = 4
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Tuning_4Hor_Vert')

if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

# Initialize output variables
tuning = np.zeros([2, N_CONTR, 2, N_SUB])
NrOfVox = np.zeros([2, N_CONTR, 2, N_SUB])
for iterSubj, su in enumerate(SUBJ):

    PATH_WINNER = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'masks')
    PATH_TMAP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'GLM', 'Hor_Vert_cluster')


    n_vox = np.zeros(2)

    for iterfu, fu in enumerate(FUNC):

        TMAPS_NII = "{}_{}_hor_vert.nii.gz".format(su, fu)
        WINNER_NII = "{}_{}_{}_winner_map.nii.gz".format(su, ROI_NAME, fu)
        ROI_NII = "{}_{}.nii.gz".format(su, ROI_NAME)

        # Read nifti tmap
        nii1 = nb.load(os.path.join(PATH_TMAP, TMAPS_NII))
        nii_tmaps = nii1.get_fdata()

        # Read nifti ROI
        nii2 = nb.load(os.path.join(PATH_WINNER, ROI_NII))
        vox_roi = nii2.get_fdata()
        idx1 = vox_roi > 0

        # Read winner map
        nii3 = nb.load(os.path.join(PATH_WINNER, 'maps', WINNER_NII))
        nii_win = nii3.get_fdata()

        if len(MASK) > 0 :

            MASK_NII = "{}_{}_{}.nii.gz".format(su, ROI_NAME, MASK[iterfu])
            nii4 = nb.load(os.path.join(PATH_MASK, MASK_NII))
            mask = nii4.get_fdata()
            mask_name = "{}_{}".format(MASK[0], MASK[1])
            idx2 = mask > 0
            idx = idx2 * idx1
        else:
            idx = idx1
            mask_name = "no_mask"

        # Extract voxel tvalue for each class and compute tuning
        vox_tvalue = nii_tmaps[idx]
        vox_label = nii_win[idx]
        n_vox[iterfu] = vox_tvalue.shape[0]

        for i, j in enumerate(range(1, 5)):
            print(j)
            vox_data = vox_tvalue[vox_label == j]
            tuning[iterfu, i, 0, iterSubj] = np.mean(vox_data, axis=0)
            #tuning[i, :, 1] = np.var(vox_data, axis=0)                # standard deviation
            tuning[iterfu, i, 1, iterSubj] = scipy.stats.sem(vox_data, axis=0)        # standard error
            NrOfVox[iterfu, i, 0, iterSubj] = vox_data.shape[0]
            NrOfVox[iterfu, i, 1, iterSubj] = vox_data.shape[0] / n_vox[iterfu] * 100

    # %% Plotting
my_dpi = 96
x = np.array([1, 2, 3, 4])
fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
contrast = ["Horizontal", "Vertical", "Diag45", "Diag135"]

for k in range(0, len(SUBJ)):
    print(k)
    axs[k].errorbar(x, tuning[0, :, 0, k], tuning[0, :, 1, k], color='black', label='BOLD')
    axs[k].errorbar(x, tuning[1, :, 0, k], tuning[1, :, 1, k], color='red', label='VASO')

    axs[k].axvspan(x[0]-0.5, x[0]+0.5, facecolor='#2ca02c', alpha=0.5)
    axs[k].set_title("Subject {}".format(k+1))
    axs[k].set_xticks(x)
    axs[k].set_ylim([-2, 2])
    axs[k].set_ylabel("T-value")
    axs[k].set_xlabel("Conditions")
    axs[k].legend();
    # fig_filename = 'allsubject_smooth_{}_{}_vmin_{}_vmax_{}.png'.format(smt_suffix, rest, my_vmin[smt], my_vmax[smt])

    # text_counts = " |BOLD: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f}|\n|VASO: H({:.0f}%) V({:.0f}%) D45({:.0f}%) D135({:.0f}%)|Tot. {:.0f}|".format(NrOfVox[0, 0, 1],
    #                                                              NrOfVox[0, 1, 1],
    #                                                              NrOfVox[0, 2, 1],
    #                                                              NrOfVox[0, 3, 1],
    #                                                              n_vox[0],
    #                                                              NrOfVox[1, 0, 1],
    #                                                              NrOfVox[1, 1, 1],
    #                                                              NrOfVox[1, 2, 1],
    #                                                              NrOfVox[1, 3, 1],
    #                                                              n_vox[1])

plt.suptitle('Tuning curves for Horizonal vs Vertical {} \n\n({})'.format(ROI_NAME, mask_name))
fig_filename = "AllSbj_Tuning_Curves_{}_{}".format(ROI_NAME, mask_name)
plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()
