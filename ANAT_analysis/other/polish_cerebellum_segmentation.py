"""Polish segmentations through morphology and smoothing."""

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-06']

PATH_SEG = os.path.join(STUDY_PATH, SUBJ[0], 'derivatives', 'anat', 'hammer_segmentator')

# Load data
nii =  nb.load(os.path.join(PATH_SEG, 'sub-06_acq-mp2rage_UNI_ss_labels_wm_pol_pol2_3_4_5_man.nii.gz'))
data = np.asarray(nii.dataobj)

# Separate tissues
# mask = data > 0
# cereb = data == 1

struct = generate_binary_structure(3, 1)  # 1 jump neighbourbhood

cereb = morphology.binary_dilation(data, structure=struct, iterations=1)
cereb = gaussian_filter(cereb.astype(float), sigma=1)
cereb = cereb > 0.5
cereb = morphology.binary_erosion(cereb, structure=struct, iterations=1)


# out = np.full(data.shape, 1)
# out[cereb != 0] += 1
# out *= mask
# Save as nift
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(cereb.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_pol.{}".format(basename, ext))

# Polish white matter
# wm = morphology.binary_dilation(wm, structure=struct, iterations=2)
# wm = gaussian_filter(wm.astype(float), sigma=1)
# wm = wm > 0.5
# wm = morphology.binary_erosion(wm, structure=struct, iterations=2)

# # Polish cerebrum
# cereb = morphology.binary_erosion(cereb, structure=struct, iterations=1)
# cereb = gaussian_filter(cereb.astype(float), sigma=1)
# cereb = cereb > 0.5
# cereb = morphology.binary_dilation(cereb, structure=struct, iterations=1)

# # Composit output image
# out = np.full(data.shape, 1)
# out[cereb != 0] += 2
# out[wm != 0] -= 1
# out *= mask

# # Save as nifti
# basename, ext = nii.get_filename().split(os.extsep, 1)
# out = nb.Nifti1Image(out.astype(int), header=nii.header, affine=nii.affine)
# nb.save(out, "{}_polished.{}".format(basename, ext))

# print('Finished.')
