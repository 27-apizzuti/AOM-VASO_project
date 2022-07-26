"""
Created on Tue Feb 22 00:26:12 2022

Create random data

@author: apizz
"""

import numpy as np
import nibabel as nb
import os

CAT = np.array([1, 2, 3, 4])

PATH_IN = 'C:\\Users\\apizz\\Desktop\\temp_LN2_UVD_FILTER\\benchmark_random\\resampled'
FILE = 'sub-02_hexbin_res_0.8'

nii = nb.load(os.path.join(PATH_IN, '{}.nii.gz'.format(FILE)))
data = np.asarray(nii.dataobj)
idx = data > 0
temp_data = data[idx]
n_vox = np.size(temp_data)

for i in range(0, n_vox):
    lab = np.random.choice(CAT)
    temp_data[i] = lab

# Put back
data[idx] = temp_data

# Save nifti
out_name = os.path.join(PATH_IN, '{}_random.nii.gz'.format(FILE))
out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
nb.save(out, out_name)

# ============================================================================
# Relabel bins with modulus trick

# nii = nb.load(os.path.join(PATH_IN, '{}.nii'.format(FILE)))
# data = np.asarray(nii.dataobj)
# data %= 4
# data += 1
# data[~idx] = 0

# # Save nifti
# out_name = os.path.join(PATH_IN, '{}_aom_modulus.nii.gz'.format(FILE))
# out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
# nb.save(out, out_name)
