# create mosaic FMR ; Starting from standard .dcm organization folder
# Run in BrainVoyager
# Run P06, P05, P04, P03, P02


import numpy as np
import os

print("Hello.")

# =============================================================================
# NIFTI input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-06"
PATH_DCM = os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', 'DICOM')
PATH_FMR = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func')
if SUBJ == "sub-04":
    seq_prefix = 'ALEPIZ20210412-'
if SUBJ == "sub-03":
    seq_prefix = 'RenHub20210212-'   #  ALEPIZ20210412- part before sequence nrs: eg -00011-0001-0001
if SUBJ == "sub-05":
    seq_prefix = 'RenHub2o210705_p05-'
if SUBJ == "sub-06":
    seq_prefix = 'RenHub2o210705_p05-'
else:
      seq_prefix = 'RENHUB_20201202 -'

option_file = '5_options_bids_fmr.txt'

# =============================================================================

# Reading Information from .txt file
info = np.loadtxt(os.path.join(STUDY_PATH, SUBJ, 'sourcedata', 'session1', option_file), dtype=str, delimiter='\t')
series = info[1:, 0]
task = info[1:, 1]
acq = info[1:, 2]
n_run = info[1:, 3]
fld = info[1:, 4]   # destination folder (func or anat)
vols = info[1:, 5]
slices = info[1:, 6]
x_dim = info[1:, 7]
y_dim = info[1:, 8]
mos_rows = info[1:, 9]
mos_cols = info[1:, 10]

for ri in range(len(series)):
    pathIn = os.path.join(PATH_DCM, str(series[ri]), seq_prefix + str(series[ri]) +'-0001-00001.dcm')
    print(pathIn)
    pathOut = os.path.join(PATH_FMR, str(task[ri]) + str(n_run[ri]))
    bids_name = SUBJ + "_task-" + str(task[ri]) + "_acq-" + str(acq[ri]) + "_run-" + str(n_run[ri])
    if not os.path.exists(pathOut):
        os.mkdir(pathOut)

    docFMR = brainvoyager.create_mosaic_fmr(pathIn, int(vols[ri]), 0, 0, int(slices[ri]), bids_name, 0, int(mos_rows[ri]), int(mos_cols[ri]), int(x_dim[ri]), int(y_dim[ri]), 2, pathOut)
    # docFMR = brainvoyager.create_fmr_dicom(pathIn, bids_name, pathOut)
