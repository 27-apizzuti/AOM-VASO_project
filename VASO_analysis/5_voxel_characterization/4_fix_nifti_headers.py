"""
Created on Fri Jan 21 18:08:40 2022
Fixing header for T-maps using ANATOMY FILE

Run WSL

@author: apizz
"""

import os
import subprocess


STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']      # , 'rightMT_Sphere16radius'

MAPS_NAME = ['_BOLD_leftMT_Sphere16radius_tmaps.nii.gz',
             '_leftMT_Sphere16radius.nii.gz', '_VASO_leftMT_Sphere16radius_tmaps.nii.gz']

for i, su in enumerate(SUBJ):

    REF_NIFTI = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'alignment_ANTs', '{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')

    for map_name in MAPS_NAME:

        in_file = "{}{}".format(su, map_name)
        command = "fslmaths "
        command += "{} ".format(REF_NIFTI)
        command += "-mul 0 "
        command += "-add "
        command += "{} ".format(os.path.join(PATH_IN, in_file))
        command += "{}".format(os.path.join(PATH_IN, in_file))

        print("{}, Fixing {} ".format(su, map_name))
        subprocess.run(command, shell=True)
