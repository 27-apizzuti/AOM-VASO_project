# preprocess FMR: slictime, moco, highpass ; AP
# This script was used to preprocess low-res functional data acquired with CMRR sequence; therefore, it includes: functional localizer and pRF mapping experiments.

import numpy as np
import os

print("Hello.")
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-06"
PATH_FMR = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func')
option_file = 'options_preprocessing_fmr.txt'
# =============================================================================
# Option file
info = np.loadtxt(os.path.join(STUDY_PATH, SUBJ, 'Options', option_file), dtype=str, delimiter='\t')
series = info[1:, 0]
task = info[1:, 1]
acq = info[1:, 2]
n_run = info[1:, 3]
fld = info[1:, 4]   # destination folder (func or anat)
vols = info[1:, 5]
slices = info[1:, 6]

# Parameters
cutoff = [6, 3, 3]

for ri in range(len(series)): #len(runnmes)):

    fmr_filename = SUBJ + '_task-' + task[ri] + '_acq-' + acq[ri] + '_run-' + n_run[ri] + '.fmr'
    docPathIn = os.path.join(PATH_FMR, task[ri] + n_run[ri], fmr_filename)
    #1 Correct Slice Timing
    docFMR = bv.open( docPathIn)
    docFMR.correct_slicetiming_using_timingtable(2) # window. sinc interpolation
    Fnme_newFMR = docFMR.preprocessed_fmr_name
    docFMR.close()

    #2 Motion Correction
    docFMR=bv.open( Fnme_newFMR)
    docFMR.correct_motion_to_run_ext(docPathIn, 1, 2, 1, 100, 1, 1)
    Fnme_newFMR = docFMR.preprocessed_fmr_name
    docFMR.close()

    #3 High-pass filtering
    docFMR=bv.open( Fnme_newFMR)
    docFMR.filter_temporal_highpass_glm_fourier(cutoff[ri])
    docFMR.close()
