"""
Created on Wed Nov  3 17:01:47 2021

Similar to pyflattenign script but specific for WINNER MAP with -VORONOI

1) Add 1 to the winner maps
2) Run patch flatten with -voronoi
3) Subtract 1 from the results

@author: apizz
"""
import os, glob
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
BINX = [532, 461, 426, 461, 568]
BINZ = [107, 103, 109, 103, 115]
CONDT = ['standard']
ROI = ['leftMT_Sphere16radius']

for iterSbj, su in enumerate(SUBJ):
    # PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2', 'winner_maps')
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2')
    os.chdir(PATH_IN)
    # for file in glob.glob('{}_{}_*_winner_map_unthreshold_fix_hd_scaled_4.nii.gz'.format(su, ROI[0])):
    for file in glob.glob('{}_{}_COMM_vox_mask_scaled_4.nii.gz'.format(su, ROI[0])):
        # 1) Add 1 to winner map
        print("Working on {}, adding 1 to {}".format(su, file))
        basename, ext = file.split(os.extsep, 1)
        output_name = os.path.join(PATH_IN, '{}_plus1.nii.gz'.format(basename))
        command = "fslmaths "
        command += "{} ".format(os.path.join(PATH_IN, file))
        command += "-add 1 "
        command += "{}".format(output_name)
        subprocess.run(command, shell=True)

        # 2) PATCH FLATTEN
        PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS[iterSbj]))
        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')

        COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
        COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
        DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

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
        print("Working on {}, removing 1 to {}".format(su, file))
        filename = '{}_plus1_binz_{}_flat_{}x{}_voronoi.nii.gz'.format(basename, BINZ[iterSbj], BINX[iterSbj], BINX[iterSbj])
        output_name = os.path.join(PATH_OUT, '{}_plus1_binz_{}_flat_{}x{}_voronoi.nii.gz'.format(basename, BINZ[iterSbj], BINX[iterSbj], BINX[iterSbj]))
        command = "fslmaths "
        command += "{} ".format(os.path.join(PATH_OUT, filename))
        command += "-sub 1 "
        command += "{}".format(output_name)
        subprocess.run(command, shell=True)
