"""
Created on Fri Dec 10 12:26:43 2021

Compoda 4 classification

NB: Only positive values

@author: apizz
"""

import nibabel as nb
import numpy as np
import os, glob
from compoda.core import closure, aitchison_norm, aitchison_dist, power

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03','sub-04', 'sub-05', 'sub-06']
ROI_NAME = ['leftMT_Sphere16radius']
FUNC = ['BOLD', 'VASO']
MAPS_NAME = ['horizontal', 'diag45', 'vertical', 'diag135']

# Reference points in simplex space
ref_array = np.asarray([
    [0.7, 0.1, 0.1, 0.1],
    [0.1, 0.7, 0.1, 0.1],
    [0.1, 0.1, 0.7, 0.1],
    [0.1, 0.1, 0.1, 0.7],
    [0.4, 0.4, 0.1, 0.1],
    [0.1, 0.4, 0.4, 0.1],
    [0.1, 0.1, 0.4, 0.4],
    [0.4, 0.1, 0.4, 0.1],
    [0.1, 0.4, 0.1, 0.4],
    [0.4, 0.1, 0.1, 0.4],
    [0.3, 0.3, 0.3, 0.1],
    [0.1, 0.3, 0.3, 0.3],
    [0.3, 0.1, 0.3, 0.3],
    [0.3, 0.3, 0.1, 0.3]])

# Scaling: make ref points lying on a sphere
anorm_ref_array = aitchison_norm(ref_array)
scal_f = anorm_ref_array[0, None] / anorm_ref_array
scal_ref_array = power(ref_array, scal_f[..., None])

# Load 4 maps
for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'compoda')

    if not os.path.exists(PATH_OUT):
        os.makedirs(PATH_OUT)  # create output folder

    os.chdir(PATH_IN)
    for itFunc in FUNC:

        print("Working on {}, {}".format(su, itFunc))

        data_tmap = []  # list with 4 3D array
        idx_mask = []

        for itMap, name_map in enumerate(MAPS_NAME):
            FILE_NAME = '{}_{}_{}_{}_t_map_fix_hd_scaled_4_binz_[0-9][0-9][0-9]_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.*'.format(su, ROI_NAME[0], itFunc, name_map)

            for file in glob.glob(FILE_NAME):
                print(file)
                nii = nb.load(os.path.join(PATH_IN, file))
                tmap = nii.get_fdata()
                idx = tmap > 0
                idx_mask.append(idx)
                data_tmap.append(tmap)

        dims = np.shape(tmap)

        # Prepare outputs
        energy = np.zeros(dims)
        aitch_norm = np.zeros(dims)
        class_vox = np.zeros(dims)

        # 3D mask
        mask = idx_mask[0] * idx_mask[1] * idx_mask[2] * idx_mask[3]  # 3D mask, it can be an external nifti
        data_tmap = np.asarray(data_tmap)
        data = np.asarray([data_tmap[0, mask], data_tmap[1, mask], data_tmap[2, mask], data_tmap[3, mask]]).T

        # Simple space
        temp_energy = np.sum(data, axis=1)
        data_baric = closure(data, k=1.0)  # vector in simplex space with barycentric coordinates
        anorm = aitchison_norm(data_baric)  # specificity

        # Compute distances

        print("Compute distance field...")
        dist_field = np.zeros((data_baric.shape[0], ref_array.shape[0]))

        for it in range(scal_ref_array.shape[0]):
            temp = np.tile(scal_ref_array[it, :, None], data_baric.shape[0]).T
            dist_field[:, it] = aitchison_dist(data_baric, temp)

        print("Classification...")
        idx_min = np.argmin(dist_field, axis=1)
        class_data = np.zeros(data_baric.shape[0])

        idx_mono = np.in1d(idx_min, [0, 1, 2, 3])
        idx_bi_cons = np.in1d(idx_min, np.arange(4, 7))
        idx_bi_jump = np.in1d(idx_min, np.arange(7, 10))
        idx_tri = np.in1d(idx_min, np.arange(10, 14))

        class_data[idx_mono] = 1
        class_data[idx_bi_cons] = 2
        class_data[idx_bi_jump] = 3
        class_data[idx_tri] = 4

        # Save output
        aitch_norm[mask] = anorm
        energy[mask] = temp_energy
        class_vox[mask] = class_data

        # Save nifti
        out_name = os.path.join(PATH_OUT, '{}_{}_{}_energy.nii.gz'.format(su, itFunc, ROI_NAME[0]))
        out = nb.Nifti1Image(energy, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)

        out_name = os.path.join(PATH_OUT, '{}_{}_{}_aitch_norm.nii.gz'.format(su, itFunc, ROI_NAME[0]))
        out = nb.Nifti1Image(aitch_norm, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)

        out_name = os.path.join(PATH_OUT, '{}_{}_{}_classification.nii.gz'.format(su, itFunc, ROI_NAME[0]))
        out = nb.Nifti1Image(class_vox, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)



print("Done.")
