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
ROI = 'leftMT_Sphere16radius'
MAPS_NAME = ['horiz', 'vert', 'diag45', 'diag135']
FUNC = ['BOLD', 'VASO']

for iterSbj, su in enumerate(SUBJ):

        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2')
        PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS[iterSbj]))

        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'patch_flatten')

        COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
        COORD_D = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
        DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

        for fu in FUNC:
            for it_map, name_map in enumerate(MAPS_NAME):
                VALUE = os.path.join(PATH_IN, '{}_{}_{}_tmaps_scaled_4_000{}.nii.gz'.format(su, fu, ROI, it_map))
                outname = os.path.join(PATH_OUT, '{}_{}_{}_tmaps_scaled_4_{}_binz_{}.nii.gz'.format(su, fu, ROI, name_map, BINZ[iterSbj]))

                command = "LN2_PATCH_FLATTEN "
                command += "-values {} ".format(VALUE)
                command += "-coord_uv {} ".format(COORD_UV)
                command += "-coord_d {} ".format(COORD_D)
                command += "-domain {} ".format(DOMAIN)
                command += "-bins_u {} ".format(BINX[iterSbj])
                command += "-bins_v {} ".format(BINX[iterSbj])
                command += "-bins_d {} ".format(BINZ[iterSbj])
                command += "-voronoi "
                command += "-output {} ".format(outname)
                subprocess.run(command, shell=True)
