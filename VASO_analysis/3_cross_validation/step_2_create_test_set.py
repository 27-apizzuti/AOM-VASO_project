"""Create test set for cross-validation.

Data preparation or fCV

Create test set for CV, copy/paste single run Nulled.nii and Not_nulled.nii in
    new folder

Input: MOCO's outputs.

Created on Thu Sep  9 11:08:22 2021

@author: apizz

Run (standard) P02, P03, P04, P05, P06
"""

import os
import glob
import nibabel as nib

print("Hello!")

# =============================================================================
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-03", "sub-04", "sub-05", "sub-06"]
PROC = 'standard'

for iterSbj in SUBJ:
    PATH_IN = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'moco')
    PATH_OUT = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'cross_validation')

    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
    # =============================================================================
    # Execution
    nn_a = glob.glob(PATH_IN + "\\Not_Nulled*a.nii")      # not nulled basis a
    n_b = glob.glob(PATH_IN + "\\Nulled_Basis*b.nii")     # nulled basis b

    nruns = len(nn_a)

    for iterRun in range(0, nruns):

        print('Processing ', iterSbj, ' run ', iterRun)

        fld_name = "run_" + str(iterRun)
        PATH_RUN = os.path.join(PATH_OUT, fld_name)

        if not os.path.exists(PATH_RUN):
            os.mkdir(PATH_RUN)

        FILE_not_nulled = nib.load(nn_a[iterRun])
        FILE_nulled = nib.load(n_b[iterRun])

        # Saving time series in a different folder
        nib.save(FILE_not_nulled, os.path.join(PATH_RUN,
                                                'Not_Nulled_Basis_a.nii.gz'))
        nib.save(FILE_nulled, os.path.join(PATH_RUN,
                                            'Nulled_Basis_b.nii.gz'))

print("Done.")
