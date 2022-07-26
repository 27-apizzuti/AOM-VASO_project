"""
Created on Wed Dec  8 18:18:28 2021

Create nifti to test composite angular map

@author: apizz
"""
import nibabel as nb
import numpy as np
import os

# REF_NIFTI = "D:\\Pilot_Exp_VASO\\pilotAOM\\sub-02\\derivatives\\anat\\patch_flatten\\sub-02_seg_rim_4_9_curvature_binned_binz_107_flat_532x532_voronoi.nii"
# PATH_OUT = "D:\\Pilot_Exp_VASO\\pilotAOM\\sub-08\\derivatives\\anat\\patch_flatten"
# MAPS_NAME = ['horizontal', 'diag45', 'vertical', 'diag135']
# FUNC = 'BOLD'
# t_value = np.asarray([4, 2, 2, 2])

# nii = nb.load(REF_NIFTI)
# cmap = nii.get_fdata()
# idx = cmap > 0
# for it, t in enumerate(t_value):
#     new_map = np.zeros(cmap.shape)
#     new_map[idx] = t
#     outname = os.path.join(PATH_OUT,"sub-08_leftMT_Sphere16radius_{}_{}_t_map_fix_hd_scaled_4_binz_107_flat_532x532_voronoi.nii.gz".format(FUNC, MAPS_NAME[it]))
#     out = nb.Nifti1Image(new_map, header=nii.header, affine=nii.affine)
#     nb.save(out, outname)

# Create 4D nifti for testing compoda

PATH_OUT = "D:\\Pilot_Exp_VASO\\pilotAOM\\sub-08\\derivatives\\anat\\patch_flatten"
MAPS_NAME = ['horizontal', 'diag45', 'vertical', 'diag135']
FUNC = 'BOLD'
map_all_axes = []

for it, t in enumerate(MAPS_NAME):
    FILE = "sub-08_leftMT_Sphere16radius_{}_{}_t_map_fix_hd_scaled_4_binz_107_flat_532x532_voronoi.nii.gz".format(FUNC, MAPS_NAME[it])
    nii = nb.load(os.path.join(PATH_OUT, FILE))
    cmap = nii.get_fdata()
    map_all_axes.append(cmap)

c = np.asarray(map_all_axes)
c = np.transpose(c, axes=(1,2,3,0))
outname = os.path.join(PATH_OUT,"sub-08_leftMT_Sphere16radius_{}_4D_maps.nii.gz".format(FUNC))
out = nb.Nifti1Image(c, header=nii.header, affine=nii.affine)
nb.save(out, outname)
