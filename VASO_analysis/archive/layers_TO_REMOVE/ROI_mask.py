"""
Created on Thu Oct 14 12:26:05 2021

Create nifti files: ROI

@author: apizz
"""

import os
import numpy as np
import bvbabel
import nibabel as nb
import subprocess


STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']      # , 'rightMT_Sphere16radius'

for roi in ROI_NAME:

    for i, su in enumerate(SUBJ):

        REF_NIFTI = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'alignment_ANTs', '{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI')

        PATH_OUT = PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'layers_columns')

        FILE_B = "{}_BOLD_interp_meanRuns_standard_ROI_{}_c_thr_4.vmp".format(su, roi)

        header_B, data_B = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_B))

        B_flat = data_B[..., 5].flatten()       # ROI

        # Extract BOLDmask
        idx = B_flat > 0
        print("{}, {}, AVG: {}".format(su, roi, np.sum(idx)))

        # Extract AVG t-map
        roi_mask = np.zeros(np.shape(B_flat))

        roi_mask[idx] = B_flat[idx]

        roi_mask = np.reshape(roi_mask, [162, 216, 26])

        # Export nifti
        outname_roi = os.path.join(PATH_IN, "{}_{}_mask.nii.gz".format(su, roi))
        img = nb.Nifti1Image(roi_mask, affine=np.eye(4))
        nb.save(img, outname_roi)

        # Commandline construction smoothing
        command = "fslmaths "
        command += "{} ".format(REF_NIFTI)
        command += "-mul 0 "
        command += "-add "
        command += "{} ".format(outname_roi)
        command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', "{}_{}_mask_fix_hd.nii.gz".format(su, roi)))
        print("{}, {}, Fixing ROI".format(su, roi))
        subprocess.run(command, shell=True)
