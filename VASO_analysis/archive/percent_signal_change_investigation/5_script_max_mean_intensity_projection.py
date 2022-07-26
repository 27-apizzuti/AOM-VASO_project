"""
Created on Mon Jul 12 18:07:38 2021
@author: apizz

Mean and max intensity projection of percent signal change

NOTES: We can choose the rest condition we want to use: Flicker or CondFix
"""
import numpy as np
import nibabel as nib
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = [ 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']          # 'sub-02', 'sub-03', 'sub-04', 'sub-05',
CONDT = ['standard']
ANAT = 'mean_run1_VASO'
brain_mask = 'mask'
FUNC = ['BOLD', 'Nulled', 'VASO_LN']
block = ["allTask"]     # "Vertical", "Horizontal", "Diag45", "Diag135"
rest = "Flicker"        # can choose between Flicker or CondFix
smooth = [0, 0.8, 1.6]

# ===========================Execute========================================
for si in SUBJ:

    anat_brain_mask_nii = nib.load(os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'brainmask', brain_mask + '.nii'))
    data_mask = anat_brain_mask_nii.get_fdata()
    for co in CONDT:
        for fu in FUNC:

            pathIN = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', co, 'ACTIVATION_v2', 'mean_blockCond_' + fu, 'perc_sign_change')
            pathOUT = os.path.join(pathIN, 'max_int_projection')

            if not os.path.exists(pathOUT):
                os.makedirs(pathOUT)

            for blk in block:
                for smt in smooth:
                    # Time averaged
                    smt_suffix = str(smt).replace(".", "pt")
                    if smt == 0:
                        act_nii = nib.load(os.path.join(pathIN, 'act_{}_{}_{}.nii.gz'.format(blk, rest, fu)))
                        masked_max_act_out_name = 'act_{}_{}_{}_max_int_proj.nii.gz'.format(blk, rest, fu)
                        masked_max_act_time_out_name = 'act_time_{}_{}_{}_max_int_proj.nii.gz'.format(blk, rest, fu)
                        act_time_nii = nib.load(os.path.join(pathIN, 'act_time_{}_{}_{}.nii.gz'.format(blk, rest, fu)))
                    else:
                        act_nii = nib.load(os.path.join(pathIN, 'smooth_{}_act_{}_{}_{}.nii.gz'.format(smt_suffix, blk, rest, fu)))
                        masked_max_act_out_name = 'smooth_{}_act_{}_{}_{}_max_int_proj.nii.gz'.format(smt_suffix, blk, rest, fu)
                        masked_max_act_time_out_name = 'smooth_{}_act_time_{}_{}_{}_max_int_proj.nii.gz'.format(smt_suffix, blk, rest, fu)
                        act_time_nii = nib.load(os.path.join(pathIN, 'smooth_{}_act_time_{}_{}_{}.nii.gz'.format(smt_suffix, blk, rest, fu)))

                    data_act = act_nii.get_fdata()
                    masked_data_act = np.multiply(data_act, data_mask)

                    # max intensity
                    max_val = np.nanmax(masked_data_act, axis=2)
                    masked_max_act_out = nib.Nifti1Image(max_val, affine=act_nii.affine)
                    nib.save(masked_max_act_out, os.path.join(pathOUT, masked_max_act_out_name))

                    # Over time
                    data_time_act = act_time_nii.get_fdata()
                    masked_data_time_act = np.multiply(data_time_act, data_mask[..., None])

                    # max intensity
                    max_val = np.nanmax(masked_data_time_act, axis=2)
                    masked_max_act_time_out = nib.Nifti1Image(max_val, affine=act_time_nii.affine)
                    nib.save(masked_max_act_time_out, os.path.join(pathOUT, masked_max_act_time_out_name))
