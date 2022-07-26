"""
Created on Mon Nov 22 18:57:57 2021
    Composite angular map
@author: apizz
"""

import os, glob
import numpy as np
import nibabel as nb
import subprocess
import math

# STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03','sub-04', 'sub-05', 'sub-06']
# SUBJ = ['sub-08']
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']
MAPS_NAME = ['horizontal', 'diag45', 'vertical', 'diag135']
FUNC = ['BOLD', 'VASO']

TEMPL = np.array([[1, 0, -1, 0], [0, 1, 0, -1]])

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
    PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'angular_map')

    os.chdir(PATH_IN)

    for itFunc in FUNC:

        x_flat_tmap = []
        y_flat_tmap = []

        for itMap, name_map in enumerate(MAPS_NAME):

            FILE_NAME = '{}_{}_{}_{}_t_map_fix_hd_scaled_4_binz_[0-9][0-9][0-9]_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.*'.format(su, ROI_NAME[0], itFunc, name_map)

            for file in glob.glob(FILE_NAME):
                print(file)
                nii = nb.load(os.path.join(PATH_IN, file))
                tmap = nii.get_fdata()
                dims = np.shape(tmap)
                idx = (tmap != 0)
                xx = tmap[idx].flatten()
                x = np.multiply(tmap[idx].flatten(), TEMPL[0,itMap])           # for each vox multiply t-value with the first coordinate
                y = np.multiply(tmap[idx].flatten(), TEMPL[1,itMap])           # y-coordinate

                x_flat_tmap.append(x)
                y_flat_tmap.append(y)

        x_flat_tmap = np.asarray(x_flat_tmap)
        y_flat_tmap = np.asarray(y_flat_tmap)


        # vector summation
        x_vect_sum = np.sum(x_flat_tmap, axis=0)
        y_vect_sum = np.sum(y_flat_tmap, axis=0)

        t = np.asarray([x_vect_sum, y_vect_sum])

        # magnitude
        magn = np.linalg.norm(t, axis=0)
        normalized_t = t /magn
        angle = np.arctan2(normalized_t[1], normalized_t[0])                # -> radians
        angle_degree = angle * 180 / np.pi
        idx2 = (angle_degree < 0)
        final_angle_degree = angle_degree
        final_angle_degree[idx2] = 360 + angle_degree[idx2]

        # final_angle_degree = (angle_degree/2) % 180

        # Save magnitude and phase as nifti
        data_mag = np.zeros(dims)
        data_ph = np.zeros(dims)

        data_mag[idx] = magn
        data_ph[idx] = final_angle_degree


        out_name = os.path.join(PATH_OUT, '{}_{}_{}_360_magn.nii.gz'.format(su, itFunc, ROI_NAME[0]))
        out = nb.Nifti1Image(data_mag, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)

        out_name = os.path.join(PATH_OUT, '{}_{}_{}_360_phase.nii.gz'.format(su, itFunc, ROI_NAME[0]))
        out = nb.Nifti1Image(data_ph, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)
