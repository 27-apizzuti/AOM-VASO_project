# -*- coding: utf-8 -*-
"""
For a study that follows BIDS specification

Dicom organization:
    Allocating dicom "series" in different folders.

    Input: dicom folder
    Output: dicom/series folders

18-04-21

AP

# Run for P06, P05, P04, P03, P02
"""

import os
import glob
from shutil import move

print("Hello!")

# =============================================================================
# DICOM input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-06"
PATH_DCM = os.fspath(os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', 'DICOM'))   # insert here the dicom folder

# =============================================================================
# Execution
f = glob.glob(PATH_DCM + "\*.dcm")
vect_series = [0] * len(f)

for i in range(len(f)):
    path, filename = os.path.split(f[i])
    basename, extension = os.path.splitext(filename)
    prefix, series, volume, measurement = basename.split('-', 3)
    vect_series[i] = series
    path_output = os.path.join(PATH_DCM, str(vect_series[i]))

    if (i > 0) and (i < len(f)-1):
        if vect_series[i+1] == vect_series[i]:
            move(f[i], path_output)
        else:   # when series changes

            if not os.path.exists(path_output):
                os.mkdir(path_output)
                print("Series number: " + vect_series[i])
            move(f[i], path_output)
    else:
        if not os.path.exists(path_output):
            os.mkdir(path_output)
            print("Series number: " + vect_series[i])
        move(f[i], path_output)

print("Success.")
