"""
Created on Mon Feb  7 18:57:51 2022
Load curvature and CV winner map
Zeroed Curvature matrix unless the bottom slice
Code sulci and gyri with (5, 6) instead of (1, 2)
Sum winner map to curvature

@author: apizz
"""
import numpy as np
import nibabel as nb
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
BINZ = [107, 103, 109, 103, 115]
BINXY=[532, 461, 426, 461, 568]
FUNC = ['BOLD', 'VASO']

for itsbj, su in enumerate(SUBJ):
    for fu in FUNC:

        FILE_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten', '{}_seg_rim_4_9_curvature_binned_binz_{}_flat_{}x{}_voronoi.nii'.format(su, BINZ[itsbj], BINXY[itsbj], BINXY[itsbj]))
        FILE2_IN = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', "{}_{}_winner_map_COL_MASK_fmedian_fmode.nii.gz".format(su, fu))
        PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data')

        # Curvature file
        nii = nb.load(FILE_IN)
        data = nii.get_fdata()

        middle_curvature = np.floor(data.shape[2]/2).astype(int)
        idxcurv = data > 0
        data[..., 0:middle_curvature-1] = 0  # zeroed
        data[..., middle_curvature+1:] = 0   # zeroed

        data[data == 1] = 5  # Sulcus (dark) 1 -> 5
        data[data == 2] = 6  # Gyrus (gray) 2 -> 6

        # Winner Map
        nii = nb.load(FILE2_IN)
        wm = nii.get_fdata()

        #Counting how many voxels have not integer class
        n = np.sum((wm > 0) * (wm <1)) + np.sum((wm > 1) * (wm < 2)) +  np.sum((wm > 2) * (wm < 3)) + np.sum((wm > 3) * (wm < 4))
        ntot = np.sum(wm > 0)
        wm[wm < 1] = 0
        wm[(wm > 1) * (wm < 2)] = 0
        wm[(wm > 2) * (wm < 3)] = 0
        wm[(wm > 3) * (wm < 4)] = 0

        # matrix trick
        wm2 = wm[..., 2:data.shape[2]]
        idxwm = wm2 > 0

        dims = np.shape(wm)
        new_data= np.zeros(dims)
        new_data[idxcurv] = 10
        new_data[..., 0:2] = data[..., middle_curvature-1:middle_curvature]

        for i in range(2, data.shape[2]-2):
            idx = wm2[..., i] > 0
            new_data[idx, i] = wm2[idx, i]

        # Saving output niftis
        out_name = os.path.join(PATH_OUT, '{}_curvature_binned_zeroed_middle_depth_to_the_bottom.nii.gz'.format(su))
        out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)

        out_name = os.path.join(PATH_OUT, '{}_{}_winner_map_COL_MASK_fmedian_fmode_plus_curvature_middle_depth_to_the_bottom.nii.gz'.format(su, fu))
        out = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)
