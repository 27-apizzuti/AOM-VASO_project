"""Create winner maps on percent signal change.

Created on Thur July 1

@author: apizz

Run (standard) P02
"""

import os
import glob
import numpy as np
import nibabel as nib

print("Hello!")

# =============================================================================
# Input path (already created)
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = "sub-02"
PROC = "standard"
UP = "4"
PATH_IN = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'ACTIVATION', 'scaled_' + UP)
PATH_OUT = os.path.join(STUDY_PATH, SUBJ, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'ACTIVATION', 'scaled_' + UP, 'winner_maps')
condition = ["Diag45", "Horizontal", "Vertical", "Diag135"]
contrast = ["BOLD", "VASO"]
thres = np.matrix([[0, 0.01], [0, 0.005]])

if not os.path.exists(PATH_OUT):
    os.makedirs(PATH_OUT)


# Execution

for iterContr in contrast:
    data = nib.load(os.path.join(PATH_IN, 'scaled_' + UP + '_act_' + condition[0] + '_' + iterContr + '_flat_flat_values.nii'))
    dims = data.get_fdata().shape
    # Put all the contrasts in a single matrix
    data_all = np.zeros(dims + (len(condition),))  # not nulled
    for iterCond in range(0, len(condition)):
        data_contr = nib.load(os.path.join(PATH_IN, 'scaled_' + UP + '_act_' + condition[iterCond] + '_' + iterContr + '_flat_flat_values.nii'))

        data_all[..., iterCond] = data_contr.get_fdata()

    winner_map = np.argmax(data_all, axis=3)+1

    winner_map = nib.Nifti1Image(winner_map, affine=data.affine, header=data.header)

    nib.save(winner_map, os.path.join(PATH_OUT, 'winner_maps_flat' + iterContr + '.nii.gz'))
