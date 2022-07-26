"""
Created on Wed Jul 14 12:19:01 2021
@author: apizz

This script compute BOLD correction from Nulled and Not Nulled (BOLD) for each condition separatly-avg. blocks (10 volumes each)

NOTES:
- Flickering block (rest) is always the same for each condition.
- Always put smooth=[0] --> to indicate that no smoothing was applyed

Run in WSL because it calls LN_BOCO (python 2_script.py)
"""

import numpy as np
import nibabel as nib
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02']          # ,'sub-03','sub-04', 'sub-05', 'sub-06'
CONDT = ['standard']
FUNC = ['BOLD', 'Nulled']
block = ["CondFix", "Flicker", "allTask"]  # ["Flicker", "allTask", "Vertical", "Horizontal", "Diag45", "Diag135"]
smooth = [0, 0.8, 1.6]

# ===========================Execute========================================
for itSbj in SUBJ:
    for itCond in CONDT:

        PATH_IN = os.path.join(STUDY_PATH, itSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', itCond, 'ACTIVATION_v2')
        PATH_OUT = os.path.join(STUDY_PATH, itSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', itCond, 'ACTIVATION_v2', 'mean_blockCond_VASO_LN')

        if not os.path.exists(PATH_OUT):
            os.makedirs(PATH_OUT)

        for itBlock in range(0, len(block)):
            for smt in range(0, len(smooth)):
                smt_suffix = str(smooth[smt]).replace(".", "pt")
                if smooth[smt] == 0:
                    nulled_filename = os.path.join(PATH_IN, 'mean_blockCond_Nulled', 'block_mean_{}_Nulled.nii.gz'.format(block[itBlock]))
                    bold_filename = os.path.join(PATH_IN, 'mean_blockCond_BOLD', 'block_mean_{}_BOLD.nii.gz'.format(block[itBlock]))
                    vaso_filename = os.path.join(PATH_OUT, 'block_mean_{}.nii.gz'.format(block[itBlock]))
                else:
                    nulled_filename = os.path.join(PATH_IN, 'mean_blockCond_Nulled', 'smooth_{}_block_mean_{}_Nulled.nii.gz'.format(smt_suffix, block[itBlock]))
                    bold_filename = os.path.join(PATH_IN, 'mean_blockCond_BOLD', 'smooth_{}_block_mean_{}_BOLD.nii.gz'.format(smt_suffix, block[itBlock]))
                    vaso_filename = os.path.join(PATH_OUT, 'smooth_{}_block_mean_{}.nii.gz'.format(smt_suffix, block[itBlock]))

                # Commandline construction LN_BOCO
                command = "LN_BOCO -Nulled "
                command += "{} ".format(nulled_filename)
                command += "-BOLD "
                command += "{} ".format(bold_filename)
                command += "-output "
                command += "{}".format(vaso_filename)

                print(command)

                # Execute command
                subprocess.run(command, shell=True)
                print("\n")
