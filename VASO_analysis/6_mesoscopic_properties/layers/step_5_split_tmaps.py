"""
Created on Thu Oct 28 14:21:14 2021

Patch Flattening script -VORONOI -DENSITY

NB: This script computes automatically the number of bin that should be used (x,y,z) once decided the "nominal (desired) resolution for the flattened domain"
Remeber to check the density file!!!

After running, move files in the right subfolder

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess
import math

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
CONDT = ['standard']
ROI_NAME = 'leftMT_Sphere16radius'

NOM_RES = 0.05   # original resolution 0.2 iso mm

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'patch_flatten')

    VALUES = [os.path.join(PATH_IN, '{}_BOLD_{}_tmaps_scaled_4.nii.gz'.format(su, ROI_NAME)),
    os.path.join(PATH_IN, '{}_VASO_{}_tmaps_scaled_4.nii.gz'.format(su, ROI_NAME))]

    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS[iterSbj]))

    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

    for j, val in enumerate(VALUES):

        # 1) Split t-maps
        print("Working on {}, split {}".format(su, val))
        basename, ext = val.split(os.extsep, 1)
        output_name = '{}'.format(basename)
        command = "fslsplit "
        command += "{} {}_ ".format(val, output_name)
        command += "-t"
        print(command)
        subprocess.run(command, shell=True)
