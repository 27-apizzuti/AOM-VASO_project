"""
Created on Wed Mar  2 10:05:00 2022

Apply columnatity index threshold to '...LN2_UVD_FILTER_columns_count_ratio.nii' (columnarity map)

@author: apizz
"""
import os
import subprocess
import numpy as np

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
threshold = np.arange(25, 100, 1)
print(threshold)

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'columns')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'columns', 'threshold')
    if not os.path.exists(PATH_OUT):
        os.makedirs(PATH_OUT)

    FILES = ['{}_{}_BOLD_FDR_BOLD_columns_full_depth_UVD_columns_mode_filter_window_count_ratio'.format(su, ROI),
         '{}_{}_BOLD_FDR_VASO_columns_full_depth_UVD_columns_mode_filter_window_count_ratio'.format(su, ROI)]

    for file_nii in FILES:
        for itThr in threshold:
            print("For {}, masking count_ratio with th={}".format(su, itThr))

            NII = os.path.join(PATH_IN, '{}.nii.gz'.format(file_nii))
            outname = os.path.join(PATH_OUT, '{}_thr_{}.nii.gz'.format(file_nii, itThr))

            command = "fslmaths {} ".format(NII)
            command += "-thr {} ".format(itThr/100)
            command += "-bin "
            command += "{} ".format(outname)

            subprocess.run(command, shell=True)
