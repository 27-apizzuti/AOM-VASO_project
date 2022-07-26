"""
Created on Mon Nov 15 16:07:46 2021
!!! FLAT
NB: Two normalization available (n. of vox shown same labes/n. of voxels I have along the depth) or (.../n. of CV voxels I have along the depth)
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
AXIS = ['Horizontal', 'Vertical', 'Diag45', 'Diag135']
MASK = "CV_AVG"
RES = 0.05  # mm

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Input Winner Maps
for itSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'patch_flatten')
    os.chdir(PATH_IN)

    for itFunc, fu in enumerate(FUNC):
        for FILE_1 in glob.glob('{}_{}_{}_winner_map_scaled_4_plus1_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(su, ROI[0], fu)):
            print('Working on {}, file {}'.format(su, FILE_1))

        # Unthresholded winner map
        nii1 = nb.load(os.path.join(PATH_IN, FILE_1))
        winner_map = nii1.get_fdata()
        dims = np.shape(winner_map)
        winner_mask = np.zeros(dims)
        winner_mask[winner_map > 0] = 1  # binary mask considering all categories

        for FILE_2 in glob.glob("{}_{}_{}_{}_mask_scaled_4_plus1_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz".format(su, ROI[0], fu, MASK)):
            print('Working on {}, file {}'.format(su, FILE_2))

        # Import CV mask
        nii2 = nb.load(os.path.join(PATH_IN, FILE_2))
        mask = nii2.get_fdata()
        idx_mask = mask > 0
        n_vox_avg_cv = np.sum(idx_mask)

        # Import thicknees file
        PATH_IN_ANAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
        os.chdir(PATH_IN_ANAT)
        for FILE_3 in glob.glob("{}_seg_rim_4_9_thickness_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii".format(su)):
            print('Working on {}, file {}'.format(su, FILE_3))

        # Import thickness
        nii3 = nb.load(os.path.join(PATH_IN_ANAT, FILE_3))
        thick = nii3.get_fdata()
        thick_avg = np.mean(thick, axis=2)

        for it, k in enumerate(range(1, 5)):

            # Create output matrices (3D)
            CI_heatmap = np.zeros(dims)  # unthreshold
            CV_CI_heatmap = np.zeros(dims)  # CV threshold

            CH_heatmap = np.zeros(dims)  # unthreshold
            CV_CH_heatmap = np.zeros(dims)  # CV threshold

            col_height = []
            CV_col_height = []

            # Unthreshold winner map columns evaluation: category binarization
            idx = winner_map == k
            temp = np.zeros(dims)  # create binary map for one category at time
            temp[idx] = 1

            # Apply CV mask
            idx2 = idx * idx_mask
            CV_temp = np.zeros(dims)  # create binary map for one category at time
            CV_temp[idx2] = 1

            for i in range(0, dims[0]):
                for j in range(0, dims[0]):

                    n_vox = np.sum(temp[i, j, :])  # number of voxels showing same category across depths
                    z_idx = temp[i, j, :] > 0
                    tot_vox = np.sum(winner_mask[i, j, :])  # number of voxels along the depth (voxels showing zero means t_Value <=0)

                    # CV maps
                    CV_n_vox = np.sum(CV_temp[i, j, :])  # number of CV voxels showing same category across depths
                    z_idx2 = CV_temp[i, j, :] > 0
                    CV_tot_vox = np.sum(mask[i, j, :])  # number of CV voxels along the depth (voxels showing zero means t_Value <=0)

                    if (n_vox > 0):  # all voxels along depth (unthresholded winner map)
                        CI_heatmap[i, j, z_idx] = (n_vox / tot_vox) * 100  # percentage with respect the whole depth
                        CH_heatmap[i, j, z_idx] = (n_vox / tot_vox) * thick_avg[i, j]
                        col_height.append((n_vox / tot_vox) * thick_avg[i, j])

                    if (CV_n_vox > 0):  # cross-validated winner map
                        CV_CI_heatmap[i, j, z_idx2] = (CV_n_vox / CV_tot_vox) * 100  # percentage with respect to the CV voxels existing along the depth.
                        CV_CH_heatmap[i, j, z_idx2] = ((CV_n_vox / tot_vox) * thick_avg[i, j])
                        CV_col_height.append((CV_n_vox / tot_vox) * thick_avg[i, j])

            # Averaging features across condition
            avg_CI = np.mean(CI_heatmap[CI_heatmap[..., 0] > 0, 0])
            avg_CH = np.mean(CH_heatmap[CH_heatmap[..., 0] > 0, 0])
            CV_avg_CI = np.mean(CV_CI_heatmap[CV_CI_heatmap[..., 0] > 0, 0])
            CV_avg_CH = np.mean(CV_CH_heatmap[CV_CH_heatmap[..., 0] > 0, 0])


            print("{}, {}, {}, averaged columnarity index (C.I.): {:.1f}%".format(su, fu, AXIS[it], avg_CI))
            print("{}, {}, {}, CV voxels averaged columnarity index (C.I.): {:.1f}%".format(su, fu, AXIS[it], CV_avg_CI))

            print("{}, {}, {}, averaged columnarity height (C.H.): {:.1f}mm".format(su, fu, AXIS[it], avg_CH))
            print("{}, {}, {}, CV voxels averaged columnarity height (C.H.): {:.1f}mm ".format(su, fu, AXIS[it], CV_avg_CH))

            # Plot and save heatmap
            out_name = os.path.join(PATH_OUT, '{}_{}_{}_{}_CI_heatmap_flat'.format(su, ROI[0], AXIS[it], fu))
            out = nb.Nifti1Image(CI_heatmap, header=nii1.header, affine=nii1.affine)
            nb.save(out, out_name)

            out_name = os.path.join(PATH_OUT, '{}_{}_{}_{}_CV_CI_heatmap_flat'.format(su, ROI[0], AXIS[it], fu))
            out = nb.Nifti1Image(CV_CI_heatmap, header=nii1.header, affine=nii1.affine)
            nb.save(out, out_name)

            # Plot and save heatmap
            out_name = os.path.join(PATH_OUT, '{}_{}_{}_{}_CH_heatmap_flat'.format(su, ROI[0], AXIS[it], fu))
            out = nb.Nifti1Image(CH_heatmap, header=nii1.header, affine=nii1.affine)
            nb.save(out, out_name)

            out_name = os.path.join(PATH_OUT, '{}_{}_{}_{}_CV_CH_heatmap_flat'.format(su, ROI[0], AXIS[it], fu))
            out = nb.Nifti1Image(CV_CH_heatmap, header=nii1.header, affine=nii1.affine)
            nb.save(out, out_name)
