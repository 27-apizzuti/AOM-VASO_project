"""
Created on Monday 21rst of January

This script applies "activation mask propagates across full cortical depth" to perimeter_chunk
e.g. BOLD_FDR_full_depth, CV_BOLD_full_depth, CV_VASO_full_depth

@author: apizz
"""
import os

import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
# SUBJ = ['sub-03', 'sub-04', 'sub-05', 'sub-06']
SUBJ = ['sub-02']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
RADIUS_DISK = [15, 13, 12, 13, 16]
# MASKS = ['BOLD_FDR', 'BOLD_CV_AVG', 'VASO_CV_AVG']
MASKS = ['COMM_vox']

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2', 'masks')
    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS_DISK[iterSbj]))

    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

    for it_mask, name_mask in enumerate(MASKS):
        print("For {}, masking perimeter chunk with {}".format(su, name_mask))

        NII_MASK = os.path.join(PATH_IN, '{}_{}_{}_mask_scaled_4_full_depth_UVD_max_filter.nii.gz'.format(su, ROI, name_mask))
        outname = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin_masked_{}_full_depth.nii.gz'.format(su, name_mask))

        command = "fslmaths {} ".format(DOMAIN)
        command += "-mas {} ".format(NII_MASK)
        command += "{} ".format(outname)

        subprocess.run(command, shell=True)
