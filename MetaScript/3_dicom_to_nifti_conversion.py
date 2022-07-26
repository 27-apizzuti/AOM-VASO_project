# -*- coding: utf-8 -*-
"""
For a study that follows BIDS specification

Dicom to Nifti conversion; data will be stored in a new "NIFTI" folder
    (function used: dcm2niix)

    Input: dicom/series folders
    Output: nifti folder

18-04-21

AP

# Run for P06, P05, P04, P03, P02
"""

import os
import subprocess

print("Hello!")

# =============================================================================
# DICOM input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-06"
PATH_DCM = os.fspath(os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', 'DICOM'))  # insert here the input dicom folder
PATH_NII = os.fspath(os.path.join(STUDY_PATH , SUBJ ,'sourcedata', 'session1','NIFTI')) # insert here the nifti output folder (to be created)

series = []


# =============================================================================

f_content = os.listdir(PATH_DCM)

if not series:
    series = f_content

# Create output directory
if not os.path.exists(PATH_NII):
    os.mkdir(PATH_NII)


# Execution
for i in range(len(series)):
    path_inputDCM = os.fspath(os.path.join(PATH_DCM, f_content[i]))
    print("Converting series {}" .format(str(f_content[i])))
    subprocess.run(["dcm2niix", "-o", PATH_NII, path_inputDCM])

print("Success.")
