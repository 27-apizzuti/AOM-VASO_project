"""
Created on Tue 13-07-2021
@author: apizz

Compute mean and standard deviation across blocks of 'averaged' run for each condition.

INPUT:

- Nulled_interp.nii, BOLD_interp.nii (averaged across runs) - output of BOCO
- P02_Pilot_AOM_run01.prt - protocol file

According to the prt file this script separate:
- 4 Axis of Motion (4 blocks for each axis)
- FLicker (16 blocks)
- CondFix (1 block)

NOTE: 10 volumes nifti is saved as output
      Multiple subjects possible
      We remove the option to find a condition-specific 'flicker' to be used for activations

(run with Spyder from Windows)
"""
import numpy as np
import nibabel as nib
import os
import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02','sub-03','sub-04', 'sub-05', 'sub-06']            # ['sub-02','sub-03','sub-04'];
CONDT = ['standard']         # ['standard', 'magn_only'];    # ['standard', 'magn_only','magn_phase']
FUNC = ['BOLD', 'Nulled']
cond = ["CondFix", "Flicker", "Horizontal", "Diag45", "Vertical", "Diag135"]

# ===========================Execute========================================
for si in SUBJ:
    for co in CONDT:
        for fu in FUNC:

            nii_file = nib.load(os.path.join(STUDY_PATH, si, 'derivatives',
                                             'func', 'AOM', 'vaso_analysis',
                                             co, 'boco', fu + '_interp.nii'))

            pathOUT = os.path.join(STUDY_PATH, si, 'derivatives', 'func',
                                   'AOM', 'vaso_analysis', co, 'ACTIVATION_v2',
                                   'mean_blockCond_' + fu)

            if not os.path.exists(pathOUT):
                os.makedirs(pathOUT)

            data = nii_file.get_fdata()
            ndims = data.shape[0:3]

            f = open(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols',
                                  si + '_Pilot_AOM_run01.prt'), "r")
            content_prt = f.read().split()

            # Dictionary structure
            my_data = {}

            for iterCond in range(0, len(cond)):      # condition loop
                # Initialize
                data_temp = []

                print("Searching volumes for condition: {}\n" .format(cond[iterCond]))
                index = content_prt.index(cond[iterCond])  # position index of "cond" in content_prt
                n = int(content_prt[index + 1])  # number of time intervals for "cond"
                start_t = index + 2  # start point of the first interval

                for iterTimes in range(0, n):
                    iterTimes_start = start_t + iterTimes
                    val_x = int(content_prt[iterTimes_start]) - 1  # -1 is for BV indexing starting from 1
                    val_y = int(content_prt[iterTimes_start + 1])

                    if val_y-val_x == 10:
                        data_temp.append(data[..., val_x:val_y])

                data_temp = np.asarray(data_temp)

                # Mean and standard deviation
                mean = np.mean(data_temp, axis=0)
                std = np.std(data_temp, axis=0)

                # Saving nifti for mean and std
                print("Saving 4D matrix {} for condition: {}\n" .format(fu, cond[iterCond]))
                img_out = nib.Nifti1Image(mean, affine=nii_file.affine)
                out_name = "block_mean_{}_{}.nii.gz".format(cond[iterCond], fu)
                nib.save(img_out, os.path.join(pathOUT, out_name))

                print("Saving 4D matrix {} for condition: {}\n" .format(fu, cond[iterCond]))
                img_out = nib.Nifti1Image(std, affine=nii_file.affine)
                out_name = "block_std_{}_{}.nii.gz".format(cond[iterCond], fu)
                nib.save(img_out, os.path.join(pathOUT, out_name))

                # Fill the dictionary
                my_data[cond[iterCond]] = copy.deepcopy(data_temp)

            if len(cond)>3:
                allTask = np.concatenate((my_data["Vertical"], my_data["Horizontal"], my_data["Diag135"], my_data["Diag45"]), axis=0)

                # Mean and standard deviation
                mean_all = np.mean(allTask, axis=0)
                std_all = np.std(allTask, axis=0)

                print("Saving 4D matrix {} for all conditions".format(fu))
                img_out = nib.Nifti1Image(mean_all, affine=nii_file.affine)
                out_name = "block_mean_allTask_{}.nii.gz" .format(fu)
                nib.save(img_out, os.path.join(pathOUT, out_name))

                print("Saving 4D matrix {} for all conditions".format(fu))
                img_out = nib.Nifti1Image(std_all, affine=nii_file.affine)
                out_name = "block_std_allTask_{}.nii.gz".format(fu)
                nib.save(img_out, os.path.join(pathOUT, out_name))
