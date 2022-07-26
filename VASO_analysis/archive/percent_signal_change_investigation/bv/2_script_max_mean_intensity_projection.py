""" Mean and max intensity projection of GLM t-values

Created on Mon Jul 12 18:07:38 2021

@author: apizz
"""

import numpy as np
import nibabel as nib
import os

# ======== Specify the input

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05','sub-06']
CONDT = ['standard']
ANAT = 'mean_run1_VASO'
brain_mask = 'mask'
FUNC = ['BOLD', 'VASO']

print("Hello!")

# ======== Execute
for si in SUBJ:

    anat_brain_mask_nii = nib.load(os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'brainmask', brain_mask + '.nii'))
    data_mask = anat_brain_mask_nii.get_fdata()
    for co in CONDT:
        pathIN = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM',
                              'vaso_analysis', co, 'GLM')

        pathOUT = os.path.join(pathIN, 'max_int_projection')

        if not os.path.exists(pathOUT):
            os.makedirs(pathOUT)

        for fu in FUNC:
                    act_nii = nib.load(os.path.join(pathIN, '{}_meanRuns_noNORDIC_bvbabel.nii.gz'.format(fu)))
                    masked_max_act_out_name = '{}_meanRuns_noNORDIC_bvbabel_max_int_proj.nii.gz'.format(fu)

                    data_act = act_nii.get_fdata()
                    masked_data_act = np.multiply(data_act, data_mask)

                    # max intensity
                    max_val = np.nanmax(masked_data_act, axis=2)
                    masked_max_act_out = nib.Nifti1Image(max_val, affine=act_nii.affine)
                    nib.save(masked_max_act_out, os.path.join(pathOUT, masked_max_act_out_name))
