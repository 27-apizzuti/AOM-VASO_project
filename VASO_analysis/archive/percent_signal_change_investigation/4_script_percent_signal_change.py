"""
Created on Wed Jul 14 16:17:29 2021
@author: apizz

This script compute percent signal change for BOLD, NULLED and VASO.
Given 'smooth array' the script works for each applied smoothing (0 refers to not smoothing)

NOTES: We can choose the rest condition we want to use: Flicker or CondFix
"""
import numpy as np
import nibabel as nib
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-05']       #'sub-02', 'sub-03', 'sub-04', 'sub-06'
CONDT = ['standard']
FUNC = ['BOLD', 'Nulled', 'VASO_LN']
block = ["allTask"]     # can isert all the conditions 'Hor', 'Vert' ...
rest = "Flicker"        # can choose between Flicker or CondFix
smooth = [0, 0.8, 1.6]

# ===========================Execute========================================
for su in SUBJ:
    for co in CONDT:
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'ACTIVATION_v2')
        for fu in FUNC:
            for smt in smooth:
                path_data = os.path.join(PATH_IN, 'mean_blockCond_' + fu)
                pathOUT = os.path.join(path_data, 'perc_sign_change')

                if not os.path.exists(pathOUT):
                    os.makedirs(pathOUT)
                smt_suffix = str(smt).replace(".", "pt")

                if smt == 0:
                    rest_nii = nib.load(os.path.join(path_data, 'block_mean_{}_{}.nii.gz'.format(rest, fu)))
                else:
                    rest_nii = nib.load(os.path.join(path_data, 'smooth_{}_block_mean_{}_{}.nii.gz'.format(smt_suffix, rest, fu)))

                rest_data = rest_nii.get_fdata()
                tmean_rest = np.mean(rest_data, axis=3)

                for iterBlock in block:
                    if (smt == 0):
                        task_nii = nib.load(os.path.join(path_data, 'block_mean_{}_{}.nii.gz'.format(iterBlock, fu)))
                    else:
                        task_nii = nib.load(os.path.join(path_data, 'smooth_{}_block_mean_{}_{}.nii.gz'.format(smt_suffix, iterBlock, fu)))

                    task_data = task_nii.get_fdata()
                    tmean_task = np.mean(task_data, axis=3)

                    if fu in ['BOLD', 'Nulled']:
                        act = (tmean_task - tmean_rest)/tmean_rest
                        act_time = (task_data - tmean_rest[..., None])/tmean_rest[..., None]
                    else:
                        act = -((tmean_task - tmean_rest)/tmean_rest)
                        act_time = -((task_data - tmean_rest[..., None])/tmean_rest[..., None])

                    print("Saving activation {} for condition: {}\n" .format(fu, iterBlock))
                    img_out = nib.Nifti1Image(act, affine=rest_nii.affine)
                    if (smt == 0):
                        out_name = "act_{}_{}_{}.nii.gz".format(iterBlock, rest, fu)
                    else:
                        out_name = "smooth_{}_act_{}_{}_{}.nii.gz".format(smt_suffix, iterBlock, rest, fu)
                    nib.save(img_out, os.path.join(pathOUT, out_name))

                    print("Saving temporal activation {} for condition: {}\n" .format(fu, iterBlock))
                    img_out = nib.Nifti1Image(act_time, affine=rest_nii.affine)
                    if smt == 0:
                        out_name = "act_time_{}_{}_{}.nii.gz".format(iterBlock, rest, fu)
                    else:
                        out_name = "smooth_{}_act_time_{}_{}_{}.nii.gz".format(smt_suffix, iterBlock, rest, fu)
                    nib.save(img_out, os.path.join(pathOUT, out_name))
