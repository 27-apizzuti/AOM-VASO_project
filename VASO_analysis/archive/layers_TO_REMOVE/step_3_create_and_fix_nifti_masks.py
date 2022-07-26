"""
Created on Thu Oct 14 17:37:55 2021
    Create nifti for special MASKS
    WSL
@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_vox", "VASO_vox", "COMM_vox", "CV_BOLD", "CV_VASO", "BOLD_FDR"]
ROI_NAME = ['leftMT_Sphere16radius']

for roi in ROI_NAME:

    # Loading groups indices
    PATH_IN = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')
    NPY = "Group_idices_BOLD_VASO_COMM_CV_BOLDfdr_{}.npy".format(roi)
    group_dict = np.load(os.path.join(PATH_IN, NPY),
                                      allow_pickle=True).item()

    for iterContr, fu in enumerate(FUNC):

        for iterSbj, su in enumerate(SUBJ):

            PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt8')
            REF_NIFTI = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'alignment_ANTs', '{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

            data = group_dict[fu][iterSbj] * 1

            # Export nifti
            print("{}, {}, exporting nifti for {}".format(su, roi, fu))
            outname = os.path.join(PATH_OUT, "{}_{}_{}_mask.nii.gz".format(su, roi, fu))
            img = nb.Nifti1Image(data, affine=np.eye(4))
            nb.save(img, outname)

            # Fix header nifti
            print("{}, {}, fixing header nifti for {}".format(su, roi, fu))
            command = "fslmaths "
            command += "{} ".format(REF_NIFTI)
            command += "-mul 0 "
            command += "-add "
            command += "{} ".format(outname)
            command += "{}".format(outname)
            subprocess.run(command, shell=True)
