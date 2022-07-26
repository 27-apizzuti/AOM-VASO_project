"""
Created on Thu Feb 17 18:00:25 2022
    Create columns benchmark nifti file
@author: apizz
"""
import numpy as np
import nibabel as nb
import os

CAT = np.array([1, 2, 3, 4])

PATH_IN = 'C:\\Users\\apizz\\Desktop\\temp_LN2_UVD_FILTER'
FILE = 'sub-02_UV_coordinates_hexbins0.5'

nii = nb.load(os.path.join(PATH_IN, '{}.nii'.format(FILE)))
data = np.asarray(nii.dataobj)
idx = data > 0
temp_data = data[idx]

cols = np.unique(temp_data)

for i in range(0, cols.size):
    lab = np.random.choice(CAT)
    idx2 = temp_data == cols[i]
    temp_data[idx2] = lab

# Put back
data[idx] = temp_data

# Save nifti
out_name = os.path.join(PATH_IN, '{}_aom.nii.gz'.format(FILE))
out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
nb.save(out, out_name)

# ============================================================================
# Relabel bins with modulus trick

nii = nb.load(os.path.join(PATH_IN, '{}.nii'.format(FILE)))
data = np.asarray(nii.dataobj)
data %= 4
data += 1
data[~idx] = 0

# Save nifti
out_name = os.path.join(PATH_IN, '{}_aom_modulus.nii.gz'.format(FILE))
out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
nb.save(out, out_name)
