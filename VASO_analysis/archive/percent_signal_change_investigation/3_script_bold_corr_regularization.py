"""
Created on Wed Jul 14 12:19:01 2021
@author: apizz

Optional script.
This script compute BOLD correction from Nulled and Not Nulled (BOLD) for each condition separatly-avg. blocks (10 volumes each)

NOTES: Here a 'regularization' is applied when performing BOLD correction
       Based on O'Brien, PlosOne, 2014 (DOI:10.1371/journal.pone.0099676)

Run in WSL because it called LN_BOCO (python 2_script.py)

"""
import numpy as np
import nibabel as nib
import os
import subprocess

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-05']
CONDT = ['standard']
FUNC = ['BOLD', 'Nulled']
block = ["allTask"]
reg = [0, 0.5, 1, 10, 100, 1000]

# ===========================Execute========================================
for itSbj in SUBJ:
    for itCond in CONDT:

        PATH_IN = os.path.join(STUDY_PATH, itSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', itCond, 'ACTIVATION_v2')
        PATH_OUT = os.path.join(STUDY_PATH, itSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', itCond, 'ACTIVATION_v2', 'vaso_reg')

        if not os.path.exists(PATH_OUT):
            os.makedirs(PATH_OUT)

        for itBlock in range(0, len(block)):
            nulled_filename = nib.load(os.path.join(PATH_IN, 'mean_blockCond_Nulled', 'block_mean_' + block[itBlock] + '_Nulled.nii.gz'))
            bold_filename = nib.load(os.path.join(PATH_IN, 'mean_blockCond_BOLD', 'block_mean_' + block[itBlock] + '_BOLD.nii.gz'))

            nulled = nulled_filename.get_fdata()
            bold = bold_filename.get_fdata()
            for r in reg:
                print(r)
                vaso = (nulled / (bold + 2*r)) + (r / (bold + 2*r))

                img_out = nib.Nifti1Image(vaso, affine=nulled_filename.affine)
                out_name = "vaso_reg_{}_{}.nii.gz".format(r, block[itBlock])
                nib.save(img_out, os.path.join(PATH_OUT, out_name))
