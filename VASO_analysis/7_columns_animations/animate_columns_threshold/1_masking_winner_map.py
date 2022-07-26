"""
Created on Thu Mar  3 10:50:11 2022

Polish with mode filter (remove 45% noise in columns)

@author: apizz
"""
import numpy as np
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [13, 12, 13, 16]
BINX = [461, 426, 461, 568]
BINZ = [103, 109, 103, 115]

FUNC = ['BOLD', 'VASO']
threshold = np.arange(25, 100, 1)

for itsbj, su in enumerate(SUBJ):

    PATH_IN = PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'patch_flatten')

    for fu in FUNC:
        FILE1 = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_{}_winner_map_scaled_4_plus1_binz_{}_flat_{}x{}_voronoi.nii.gz'.format(su, fu, BINZ[itsbj], BINX[itsbj], BINX[itsbj]))

        for  itThr in threshold:
            MASK = os.path.join(PATH_IN, 'columns_threshold', '{}_leftMT_Sphere16radius_BOLD_FDR_{}_columnar_mask_thr_{}_plus1_binz_{}_flat_{}x{}_voronoi.nii'.format(su, fu, itThr, BINZ[itsbj], BINX[itsbj], BINX[itsbj]))

            PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'columns_threshold')
            if not os.path.exists(PATH_OUT):
                os.makedirs(PATH_OUT)

            print('For {} masking {} with {}'.format(su, fu, itThr))
            outname = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_{}_winner_map_{}_COL_MASK.nii.gz'.format(su, fu, itThr))

            command = "fslmaths "
            command += "{} ".format(FILE1)
            command += "-mas {} ".format(MASK)
            command += "{} ".format(outname)

            subprocess.run(command, shell=True)
