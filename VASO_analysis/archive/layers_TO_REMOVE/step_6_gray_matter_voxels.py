"""
    Created on Thu Oct 28 13:30:13 2021
    Create gray matter mask from rim file.
    Apply the mask to the CV-voxels for BOLD and VASO.

    @author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_CV_AVG", "VASO_CV_AVG"]
ROI_NAME = ['leftMT_Sphere16radius']

for iterSbj, su in enumerate(SUBJ):

    PATH_ANAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'segmentation_4')
    SEG_FILE = os.path.join(PATH_ANAT, '{}_scaled_4_seg_rim.nii.gz'.format(su))
    OUTNAME = os.path.join(PATH_ANAT, '{}_scaled_4_gray_matter_rim.nii.gz'.format(su))

    # Create Gray Matter Mask
    print("For {}, Creating gray matter mask".format(su))
    command = "fslmaths "
    command += "{} ".format(SEG_FILE)
    command += "-thr 3 "
    command += "-bin "
    command += "{}".format(OUTNAME)
    subprocess.run(command, shell=True)

    for iterMask, mask in enumerate(FUNC):

        PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2')

        # Load nifti and count initial n. of voxels
        NII_FILE = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4.nii.gz'.format(su, ROI_NAME[0], mask))
        nii1 = nb.load(NII_FILE)
        vox_mask = nii1.get_fdata()
        nvox = np.sum(vox_mask > 0)
        print("For {}, {}, tot. n. of voxels: {}".format(su, mask, nvox))

        # Apply gray matter mask
        outname_vox = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4_gray_matter.nii.gz'.format(su, ROI_NAME[0], mask))
        print("For {}, Applying gray matter mask".format(su))
        command = "fslmaths "
        command += "{} ".format(NII_FILE)
        command += "-mas "
        command += "{} ".format(OUTNAME)
        command += "{}".format(outname_vox)
        subprocess.run(command, shell=True)

        # Load masked nifti and count the updated n. of voxels
        nii2 = nb.load(os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4_gray_matter.nii.gz'.format(su, ROI_NAME[0], mask)))
        vox_mask2 = nii2.get_fdata()
        nvox2 = np.sum(vox_mask2 > 0)
        print("For {}, {}, n. of voxels in gray matter: {}, {}%".format(su, mask, nvox2, (nvox2/nvox)*100))
