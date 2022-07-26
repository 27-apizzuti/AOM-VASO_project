"""
Created on Monday 21rst of January

This script propagates a binary activation mask across the full cortical depth.
LN2_UVD_FILTER -max (Laynii)
e.g. BOLD_FDR, CV_BOLD, CV_VASO

@author: apizz
"""
import os, glob
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS_DISK = [15, 13, 12, 13, 16]
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
MASKS = ['BOLD_FDR', 'BOLD_CV_AVG', 'VASO_CV_AVG']
# MASKS = ['COMM_vox']

# Program parameter (cylinder)
RADIUS = 0.39  # nominal resolution
HEIGHT = 2

#--------------------------------------
for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2', 'masks')
    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS_DISK[iterSbj]))

    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))
    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))

    for it_mask, name_mask in enumerate(MASKS):
        print("For {}, propagating {}".format(su, name_mask))

        VALUE = os.path.join(PATH_IN, '{}_{}_{}_mask_scaled_4.nii.gz'.format(su, ROI, name_mask))
        outname = os.path.join(PATH_IN, '{}_{}_{}_mask_scaled_4_full_depth.nii.gz'.format(su, ROI, name_mask))

        command = "LN2_UVD_FILTER "
        command += "-values {} ".format(VALUE)
        command += "-coord_uv {} ".format(COORD_UV)
        command += "-coord_d {} ".format(COORD_D)
        command += "-domain {} ".format(DOMAIN)
        command += "-radius {} ".format(RADIUS)
        command += "-height {} ".format(HEIGHT)
        command += "-max "
        command += "-output {} ".format(outname)
        subprocess.run(command, shell=True)
