"""
Created on Wed Feb 16 11:32:37 2022
!!! FLAT
Create columns map
Input:
    1) CH per condition
    2) winner map
Output:
    1) comulative plot
    2) new mask for winner maps

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
import matplotlib.pyplot as plt

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
# SUBJ = ['sub-02', 'sub-03']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Columns')
AXIS = ['Horizontal', 'Vertical', 'Diag45', 'Diag135']
MASK = "CV_AVG"
PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Columns')
thr = 75

# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
fig.suptitle('Columns as function of CI')

for itFu, fu in enumerate(FUNC):
    for itSbj, su in enumerate(SUBJ):

        idx_list = []

        for itAxis, cond in enumerate(AXIS):

            FILE_1 = "{}_{}_{}_{}_CI_heatmap_flat.nii".format(su, ROI[0], cond, fu)
            nii1 = nb.load(os.path.join(PATH_IN, FILE_1))

            CI_map = nii1.get_fdata()
            dims = np.shape(CI_map)
            idx = CI_map > 0   # where I have voxels
            CI_count = CI_map[idx]  # Take the non-zeros

            # Thresholding
            idx2 = CI_map > thr
            idx_list.append(idx2*idx)

            # Parametric plot
            threshold = np.linspace(51, 99, num=49, dtype='int32')
            c50 = np.sum(CI_count > 50)
            par_count = []
            for i, j in enumerate(threshold):
                par_count.append(np.sum(CI_count > threshold[i])/c50 * 100)

            y = np.asarray(par_count)

            # Plotting
            axs[itFu, itSbj].plot(threshold, y)
            axs[itFu, itSbj].legend(AXIS)
            axs[itFu, itSbj].set_xlabel("CI threshold")
            axs[itFu, itSbj].set_ylabel("% of columns")
            axs[itFu, itSbj].set_title("{} {}".format(su, fu))
            if itAxis == 3:
                axs[itFu, itSbj].axvline(thr, color='k', linestyle='dashed', linewidth=1)

                # Create a column mask
                col_mask = np.zeros(dims)
                temp = idx_list[0] + idx_list[1] + idx_list[2] + idx_list[3]

                col_mask[temp, :] = 1

                # Save nifti mask
                out_name = os.path.join(PATH_OUT, '{}_{}_{}_mask_columns_CI_{}'.format(su, ROI[0], fu, thr))
                out = nb.Nifti1Image(col_mask, header=nii1.header, affine=nii1.affine)
                nb.save(out, out_name)

plt.savefig(os.path.join(PATH_OUT,'{}_Columns_vs_CI_AllSbj_thr_{}.jpeg'.format(ROI[0], thr)), bbox_inches='tight')
plt.savefig(os.path.join(PATH_OUT,'{}_Columns_vs_CI_AllSbj_thr_{}.svg'.format(ROI[0], thr)), bbox_inches='tight')
