"""
Created on Sun Oct  3 10:09:34 2021

Create fake VMP for testing

@author: apizz
"""
import os
import numpy as np
import bvbabel

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
PATH_IN = os.path.join(STUDY_PATH, 'sub-08', 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', 'standard', 'cross_validation', 'run_2', 'GLM', 'ROI')
PATH_IN2 = os.path.join(STUDY_PATH, 'sub-08', 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', 'standard', 'cross_validation', 'run_1', 'GLM', 'ROI')
FILE_IN = 'sub-08_VASO_interp_LN_meanRuns_standard_ROI_leftMT_Sphere16radius.vmp'
IN_FILE = os.path.join(PATH_IN, FILE_IN)

header_sx, data_sx = bvbabel.vmp.read_vmp(os.path.join(PATH_IN2, FILE_IN))

header_dx, data_dx = bvbabel.vmp.read_vmp(IN_FILE)

idx_dx = data_dx[..., 4]>0
idx_sx = data_sx[..., 4]>0

data_dx -= 150

bvbabel.vmp.write_vmp(IN_FILE, header_dx, data_dx)
