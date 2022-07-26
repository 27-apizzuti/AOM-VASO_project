"""
Created on Fri Jul 16 17:37:35 2021
@author: apizz

This script applies gaussian smoothing ('fslmaths')

It will be run for BOLD and Nulled before creating VASO_LN:

(Run in WSL-python .py)

"""
import os
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'Nulled']
block = ["CondFix", "Flicker", "allTask"]
smooth = [0.8, 1.6]

# ===========================Execute========================================
for su in SUBJ:
    for co in CONDT:
        for fu in FUNC:
            PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func',
                                   'AOM', 'vaso_analysis', co, 'ACTIVATION_v2', 'mean_blockCond_' + fu)
            for blk in block:
                for smt in smooth:
                    smt_suffix = str(smt).replace(".", "pt")
                    data2smooth = os.path.join(PATH_IN, 'block_mean_{}_{}.nii.gz'.format(blk, fu))
                    data_out = os.path.join(PATH_IN, 'smooth_{}_block_mean_{}_{}.nii.gz'.format(smt_suffix, blk, fu))

                    # Commandline construction smoothing
                    command = "fslmaths "
                    command += "{} ".format(data2smooth)
                    command += "-s "
                    command += "{} ".format(smt)
                    command += "{}".format(data_out)

                    print(command)

                    # Execute command
                    subprocess.run(command, shell=True)
                    print("\n")
