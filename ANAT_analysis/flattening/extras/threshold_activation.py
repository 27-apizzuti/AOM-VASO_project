# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 15:30:10 2021

@author: apizz
"""

""" Thresholding activation (percent signal change)

The script uses fslmaths called as a subprocess

(It works on Linux-subsystem, run: python .py)
"""

import os
import subprocess
import numpy as np
import nibabel as nb

print("Hello!")

# =============================================================================
# Input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-02"
PROC = "standard"
UP = "4"
PATH_IN = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'ACTIVATION', 'scaled_' + UP)
PATH_OUT = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'ACTIVATION', 'scaled_' + UP, 'masked_act_flat')
condition = ["Diag45", "Horizontal", "Vertical", "Diag135"]
contrast = ["BOLD", "VASO"]
thres = np.matrix([[0, 0.01], [0, 0.005]])

if not os.path.exists(PATH_OUT):
    os.makedirs(PATH_OUT)

# =============================================================================

# Execution

for iterContr in range(0, len(contrast)):
    for iterCond in range(0, len(condition)):
        in_act_path = os.path.join(PATH_IN, 'scaled_' + UP + '_act_' + condition[iterCond] + '_' + contrast[iterContr] + '_flat_flat_values.nii')
        out_act_path = os.path.join(PATH_OUT, 'scaled_' + UP + '_act_' + condition[iterCond] + '_' + contrast[iterContr] + '_flat_flat_values_masked.nii')

        # Commandline fslmaths thresholding
        command = "fslmaths "
        command += "{} ".format(in_act_path)
        command += "-thr "
        command += "{} ".format(thres[iterContr, 0])
        command += "-uthr "
        command += "{} ".format(thres[iterContr, 1])
        command += "{} ".format(out_act_path)

        print(command)

        # Execute command
        # subprocess.run(command, shell=True)
