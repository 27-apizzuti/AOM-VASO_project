"""
Created on Mon Nov 15 16:07:46 2021
!!! FLAT
NB: Change the normalization (n. of vox shown same labes/n. of voxels I have along the depth)
Columns in a flat representation

@author: apizz
"""

import glob
import numpy as np
import nibabel as nb
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Columns')
AXIS = ['Horizontal', 'Verical', 'Diag45', 'Diag135']
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Input Winner Maps
for itSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten', 'unthresholded_maps')
    os.chdir(PATH_IN)

    for itFunc, fu in enumerate(FUNC):
        for FILE_2 in glob.glob('{}_{}_{}_winner_map_unthreshold_fix_hd_scaled_4_plus1_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(su, ROI[0], fu)):
            print('Working on {}, file {}'.format(su, FILE_2))
        nii2 = nb.load(os.path.join(PATH_IN, FILE_2))
        winner_map = nii2.get_fdata()
        dims = np.shape(winner_map)
        winner_mask = np.zeros(dims)
        winner_mask[winner_map > 0] = 1  # binary mask considering all categories

        # Create heatmap for columns
        heatmap = np.zeros((dims[0], dims[0], 4))
        heatmap2 = np.zeros((dims[0], dims[0], 4))
        temp_depth = np.zeros((dims[0], dims[0], 4))
        for it, k in enumerate(range(1, 5)):
            # print("Evaluating columns for condition: {}".format(k))
            idx = winner_map == k
            temp = np.zeros(dims)  # create binary map for one category at time
            temp[idx] = 1

            for i in range(0, dims[0]):
                for j in range(0, dims[0]):
                    temp2 = np.sum(temp[i, j, :])  # number of voxels showing same category across depths
                    temp3 = np.sum(winner_mask[i, j, :])  # number of CV voxels along the depth
                    if (temp2 > 0):
                        heatmap[i, j, it] = (temp2 / dims[-1]) * 100
                        heatmap2[i, j, it] = (temp2 / temp3) * 100
                        temp_depth[i, j, it] = temp3/dims[-1] * 100

            idx_col = heatmap2[..., it] > 0
            idx_depth = temp_depth[..., it] > 0

            avg_col = np.mean(heatmap2[idx_col, it])
            avg_depth = np.mean(temp_depth[idx_depth, it])

            print("{}, {}, {}, averaged columnarity index: {} ({})".format(su, fu, AXIS[it], avg_col, avg_depth))
            # out_name = os.path.join(PATH_OUT, '{}_{}_{}_heatmap_columns_{}_flat_ref_{}'.format(su, ROI[0], AXIS[it], fu, dims[-1]))
            # out = nb.Nifti1Image(heatmap, header=nii2.header, affine=nii2.affine)
            # nb.save(out, out_name)

            # out_name = os.path.join(PATH_OUT, '{}_{}_{}_heatmap_columns_{}_flat'.format(su, ROI[0], AXIS[it], fu))
            # out = nb.Nifti1Image(heatmap2, header=nii2.header, affine=nii2.affine)
            # nb.save(out, out_name)

        # stat_columns[itSbj, itFunc, k-1] = np.max(heatmap[heatmap > 50])

# out_name = os.path.join(PATH_OUT, 'AllSbj_avg_heatmap_columns_flat')
# out = nb.Nifti1Image(stat_columns, header=nii2.header, affine=nii2.affine)
# nb.save(out, out_name)
