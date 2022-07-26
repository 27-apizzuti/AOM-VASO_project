# -*- coding: utf-8 -*-
"""
For a study that follows BIDS specification

    Rename Nifti files (e.g. High-res functional data SS-SI VASO or anat data)

    Input: nifti folder
    Output: nifti/func or anat

18-04-21

AP
# Run for P06, P05, P04, P03, P02
"""
import os
import pandas as pd

print("Hello!")

# =============================================================================
# NIFTI input path (already created)

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-06"
PATH_NII = os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', 'NIFTI')
option_file = '4_options_bids_nifti.txt'
# =============================================================================

# Reading Information from .txt file
info = pd.read_csv(os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', option_file), sep='\t', header=None)

series = list(info.loc[1:, 0])
task = list(info.loc[1:, 1])
acq = list(info.loc[1:, 2])
n_run = list(info.loc[1:, 3])
fld = list(info.loc[1:, 4])  # destination folder (func or anat)


f_content = os.listdir(PATH_NII)

for i in range(len(f_content)):

    basename, extension = os.path.splitext(f_content[i])
    b = basename.split('_')

    if b[0] in series:
        print("Renaming series {}" .format(str(b[0])))
        k = series.index(b[0])
        if fld[k] == 'func':
            bids_name = SUBJ + "_task-" + str(task[k]) + "_acq-" + str(acq[k]) + "_run-" + str(n_run[k]) + extension
        else:
            bids_name = SUBJ + "_acq-" + str(acq[k]) + "_" + str(n_run[k]) + extension
        if not os.path.exists(os.path.join(PATH_NII, fld[k])):
            os.mkdir(os.path.join(PATH_NII, fld[k]))
        path_old = os.fspath(os.path.join(PATH_NII, f_content[i]))
        path_new = os.fspath(os.path.join(PATH_NII, fld[k], bids_name))
        os.rename(path_old, path_new)

print("Success.")
