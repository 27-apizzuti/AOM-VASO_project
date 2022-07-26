"""
Created on Fri Apr 22 18:06:51 2022
Extract layer 9 as boundary for Fig.5
@author: apizz
"""
import numpy as np
import nibabel as nb
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUB = 'sub-02'
FILE_IN = os.path.join(STUDY_PATH, SUB, 'derivatives', 'anat', 'layers_4', 'sub-02_seg_rim_4_9_layers_equivol.nii')
nii = nb.load(FILE_IN)
data = nii.get_fdata()

new_data = np.zeros(np.shape(data))
idx = data == 2
new_data[idx] = 1

out_name = os.path.join(STUDY_PATH, SUB, 'derivatives', 'anat', 'layers_4', 'sub-02_seg_rim_4_9_extract_layer2')
out = nb.Nifti1Image(new_data, header=nii.header, affine=nii.affine)
nb.save(out, out_name)
