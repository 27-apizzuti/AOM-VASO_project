"""
Created on Thu Mar  3 10:50:11 2022
Polish with mode filter 
@author: apizz
"""

import numpy as np
import nibabel as nb
from scipy import stats
import os

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02']
FUNC = ['consistent']
threshold = np.arange(25, 91, 1)

for itsbj, su in enumerate(SUBJ):
    for fu in FUNC:
        PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'consistent_columns', 'polished_columns')
        PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'consistent_columns', 'polished_columns_2')
        if not os.path.exists(PATH_OUT):
            os.makedirs(PATH_OUT)

        for it in threshold:
            FILE = os.path.join(PATH_IN, '{}_leftMT_Sphere16radius_{}_winner_map_{}_COL_MASK_fmedian.nii.gz'.format(su, fu, it))
            print("For {}, {}, threshold = {}".format(su, fu, it))
            # Winner Map
            nii = nb.load(FILE)
            wm = nii.get_fdata()
            new_wm = np.zeros(wm.shape)
            thr = np.floor(wm.shape[2]*it/100)
            c = stats.mode(wm, axis=2)

            # Polish
            for it1 in range(0, wm.shape[0]):
                for it2 in range(0, wm.shape[0]):
                    temp_wm = wm[it1, it2, :]
                    mode = c[0][it1, it2]
                    count = c[1][it1, it2]
                    if mode > 0:
                        if count > thr:
                            idx = temp_wm == mode
                            new_wm[it1, it2, idx] = mode

            # Save nifti
            out_name = os.path.join(PATH_OUT, '{}_leftMT_Sphere16radius_{}_winner_map_{}_COL_MASK_fmedian_fmode.nii.gz'.format(su, fu, it))
            out = nb.Nifti1Image(new_wm, header=nii.header, affine=nii.affine)
            nb.save(out, out_name)
