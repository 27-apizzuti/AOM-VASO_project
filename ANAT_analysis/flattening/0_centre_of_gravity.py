"""
Created on Thu Oct 28 14:21:14 2021

Before Multilaterate: find the centre of mass of activated regions

It will be used as initial "control_point_0"

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-04']
CONDT = ['standard']
FUNC = ["BOLD_CV_AVG"]         # "VASO_CV_AVG"
ROI_NAME = ['leftMT_Sphere16radius']

# 1) Create a binary mask of perimeter_chunk
PATH_FLA = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_{}'.format(radius, cp))
PER_FILE = os.path.join(PATH_FLA, '{}_perimeter_chunk.nii'.format(SUBJ[0]))
MAS_FILE = os.path.join(PATH_FLA, '{}_perimeter_chunk_mask.nii'.format(SUBJ[0]))

PATH_MASK = os.path.join(STUDY_PATH, SUBJ[0], 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2')
MASK_FILE = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4_gray_matter.nii.gz'.format(SUBJ[0], ROI_NAME[0], FUNC[0]))

# 2) Centre of mass
print("For {}, Looking for centroid".format(SUBJ[0]))
command = "fslstats "
command += "{} ".format(MASK_FILE)
command += "-C "
subprocess.run(command, shell=True)
