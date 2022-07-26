"""
Created on Fri Jan 21 18:08:40 2022
Fixing header for T-maps using ANATOMY FILE

Run WSL (python .py)

@author: apizz
"""

import os
import subprocess


STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ["sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']      # , 'rightMT_Sphere16radius'

MAPS_NAME = ['_BOLD_hor_vert.nii.gz',
             '_VASO_hor_vert.nii.gz']

for i, su in enumerate(SUBJ):

    REF_NIFTI = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'alignment_ANTs', '{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'GLM', 'Hor_Vert_cluster')

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
