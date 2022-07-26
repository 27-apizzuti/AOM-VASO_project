"""
Created on Wed Mar  2 12:30:15 2022

Similar to pyflattenign script but specific for MASK with -VORONOI
Flattening 'thresholded_columnarity_map' for a range of thresholds
@author: apizz
"""

import os
import subprocess
import numpy as np

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
BINX = [532, 461, 426, 461, 568]
BINZ = [107, 103, 109, 103, 115]
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
FUNC = ['BOLD', 'VASO']
threshold = np.arange(25, 100, 1)

for iterSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'columns', 'threshold')

    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS[iterSbj]))
    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'patch_flatten', 'columns_threshold')
    if not os.path.exists(PATH_OUT):
        os.makedirs(PATH_OUT)

    for fu in FUNC:
        for itThr in threshold:

            VALUE = os.path.join(PATH_IN, '{}_{}_BOLD_FDR_{}_columns_full_depth_UVD_columns_mode_filter_window_count_ratio_thr_{}.nii.gz'.format(su, ROI, fu, itThr))
            basename = '{}_{}_BOLD_FDR_{}_columnar_mask_thr_{}'.format(su, ROI, fu, itThr)

            # 1) Add 1 to mask
            print("Working on {}, adding 1 to {}".format(su, VALUE))
            output_name = os.path.join(PATH_IN, '{}_plus1.nii.gz'.format(basename))
            command = "fslmaths "
            command += "{} ".format(VALUE)
            command += "-add 1 "
            command += "{}".format(output_name)
            subprocess.run(command, shell=True)

            # 2) PATCH FLATTEN
            outname = os.path.join(PATH_OUT, '{}_plus1_binz_{}.nii.gz'.format(basename, BINZ[iterSbj]))
            command = "LN2_PATCH_FLATTEN "
            command += "-values {} ".format(output_name)
            command += "-coord_uv {} ".format(COORD_UV)
            command += "-coord_d {} ".format(COORD_D)
            command += "-domain {} ".format(DOMAIN)
            command += "-bins_u {} ".format(BINX[iterSbj])
            command += "-bins_v {} ".format(BINX[iterSbj])
            command += "-bins_d {} ".format(BINZ[iterSbj])
            command += "-voronoi "
            command += "-output {} ".format(outname)
            subprocess.run(command, shell=True)

            # 3) Subtract 1 to the results
            print("Working on {}, removing 1 to {}".format(su, VALUE))
            filename = '{}_plus1_binz_{}_flat_{}x{}_voronoi.nii.gz'.format(basename, BINZ[iterSbj], BINX[iterSbj], BINX[iterSbj])
            output_name = os.path.join(PATH_OUT, '{}_plus1_binz_{}_flat_{}x{}_voronoi.nii.gz'.format(basename, BINZ[iterSbj], BINX[iterSbj], BINX[iterSbj]))
            command = "fslmaths "
            command += "{} ".format(os.path.join(PATH_OUT, filename))
            command += "-sub 1 "
            command += "{}".format(output_name)
            subprocess.run(command, shell=True)
