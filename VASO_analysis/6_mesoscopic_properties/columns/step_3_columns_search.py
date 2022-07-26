"""
Created on Monday 21rst of January

Compute columnarity index map 

LN2_UVD_FILTER -columns

Input parameters:
    RADIUS = 0.6
    HEIGHT = 2

@author: apizz
"""
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
RADIUS_DISK = [15, 13, 12, 13, 16]
MASKS = ['BOLD_FDR', 'BOLD_CV_AVG', 'VASO_CV_AVG']

# Program parameter (cylinder)
RADIUS = 0.6  # diameter spans the effective resolution (0.8mm)
HEIGHT = 2

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2', 'maps')

    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'columns')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS_DISK[iterSbj]))
    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))

    for it_mask, name_mask in enumerate(MASKS):

        DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin_masked_{}_full_depth.nii.gz'.format(su, name_mask))

        if (name_mask=='BOLD_FDR'):
            FUNC = ['BOLD', 'VASO']
        elif (name_mask=='COMM_vox'):
            FUNC = ['BOLD', 'VASO']
        elif (name_mask=='BOLD_CV_AVG'):
            FUNC = ['BOLD']
        else:
            FUNC = ['VASO']
        for fu in FUNC:
            print("For {}, {}, searching columns in per_chunck masked with {}".format(su, fu, name_mask))

            VALUE = os.path.join(PATH_IN, '{}_{}_{}_winner_map_scaled_4.nii.gz'.format(su, ROI, fu))
            outname = os.path.join(PATH_OUT, '{}_{}_{}_{}_columns_full_depth.nii.gz'.format(su, ROI, name_mask, fu))

            command = "LN2_UVD_FILTER "
            command += "-values {} ".format(VALUE)
            command += "-coord_uv {} ".format(COORD_UV)
            command += "-coord_d {} ".format(COORD_D)
            command += "-domain {} ".format(DOMAIN)
            command += "-radius {} ".format(RADIUS)
            command += "-height {} ".format(HEIGHT)
            command += "-columns "
            command += "-output {} ".format(outname)
            subprocess.run(command, shell=True)
