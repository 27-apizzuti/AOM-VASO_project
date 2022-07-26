"""
Created on Thu Mar  3 10:50:11 2022
Polish with median filter
@author: apizz
"""
import numpy as np
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02']
FUNC = ['BOLD']
threshold = np.arange(29, 100, 1)

for itsbj, su in enumerate(SUBJ):
    PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'columns_threshold', 'polished_columns')
    if not os.path.exists(PATH_OUT):
        os.makedirs(PATH_OUT)
    for fu in FUNC:
        for  itThr in threshold:
            FILE = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'columns_threshold', '{}_leftMT_Sphere16radius_{}_winner_map_{}_COL_MASK.nii.gz'.format(su, fu, itThr))

            print('For {} {} with {}, apply median filter'.format(su, fu, itThr))
            outname = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_{}_winner_map_{}_COL_MASK_fmedian.nii.gz'.format(su, fu, itThr))

            command = "fslmaths "
            command += "{} ".format(FILE)
            command += "-kernel boxv3 5 5 41 "
            command += "-fmedian {}".format(outname)

            subprocess.run(command, shell=True)
