"""
Leave one run out Cross-Validation
Step_2:
    - Voxel selection across folds.
    - Voxels selection using AVG labels (after cluster thresholding)
Created on Thu Sep 16 10:48:56 2021
@author: apizz
"""

import os
import numpy as np
import bvbabel
from copy import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']
tag = 'c_thr_4'
VASO_BOLD_MASK = False

for su in SUBJ:
    for roi in ROI_NAME:
        for fu in FUNC:
            print("Working on {}, {}, {}".format(su, roi, fu))
            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

            # Load AVG results from Winner_Maps
            PATH_AVG = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'GLM', 'ROI')

            NPZ_AVG = '{}_{}_meanRuns_{}_ROI_{}_{}{}_tuning_dict.npy'.format(su, fu, CONDT[0], roi, tag, mask_suffix)
            VMP_AVG = '{}_{}_meanRuns_{}_ROI_{}_{}{}_preference_metrics.vmp'.format(su, fu, CONDT[0], roi, tag, mask_suffix)

            IN_FILE_AVG = os.path.join(PATH_AVG, VMP_AVG)

            avg_tuning_dict = np.load(os.path.join(PATH_AVG, NPZ_AVG),
                                          allow_pickle=True).item()
            header_avg, data_avg = bvbabel.vmp.read_vmp(IN_FILE_AVG)

            # AVG voxels --> map #2
            matrix_avg = data_avg[..., 1]
            idx_avg = matrix_avg > 0                                               # // AVG voxels indices referred to VMP (3D, boolean)
            AVG_VOX = matrix_avg[idx_avg]                                          # // AVG voxels labels (1D, float)
            n_avg = len(AVG_VOX)                                                   # // n. of AVG voxels

            # Load CV results step 1
            PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', CONDT[0], 'cross_validation', 'Results')

            NPZ_CV = "{}_{}_{}_cv_step1_dict.npy".format(su, fu, roi)

            cv_tuning_dict = np.load(os.path.join(PATH_CV, NPZ_CV),
                                          allow_pickle=True).item()
            n_cv_flds = cv_tuning_dict["n_folds"]

            # Extract CV labels
            CV_VOX = np.zeros([n_avg, n_cv_flds])
            bool_cv_avg = np.zeros([n_avg, n_cv_flds])
            for iterFLD in range(0, n_cv_flds):

                CV_VOX[:, iterFLD] = cv_tuning_dict["Labels"][iterFLD][idx_avg]    # // extract CV voxels by using AVG vox indices (3/4D)
                bool_cv_avg[:, iterFLD] = CV_VOX[:, iterFLD] == AVG_VOX            # // Compare CV vs AVG (3/4D boolean)

            temp = np.sum(bool_cv_avg, axis=1)                                     # // sum across CV folds
            idx_cv_avg = temp > 0                                                  # // CV-AVG voxels indices 1D (boolean)
            CV_AVG_VOX = copy(AVG_VOX)
            CV_AVG_VOX[idx_cv_avg == False] = 0                                    # // mantain only CV-AVG voxels
            n_cv_avg = np.sum(idx_cv_avg)

            # CV-AVG
            hor = np.count_nonzero(CV_AVG_VOX == 1)
            vert = np.count_nonzero(CV_AVG_VOX == 2)
            diag45 = np.count_nonzero(CV_AVG_VOX == 3)
            diag135 = np.count_nonzero(CV_AVG_VOX == 4)

            # AVG
            hor_avg = np.count_nonzero(AVG_VOX == 1)
            vert_avg = np.count_nonzero(AVG_VOX == 2)
            diag45_avg = np.count_nonzero(AVG_VOX == 3)
            diag135_avg = np.count_nonzero(AVG_VOX == 4)

            print("From AVG: {} --> CV-AVG: {} ({}%)".format(n_avg, n_cv_avg, int(n_cv_avg*100/n_avg)))
            # print("For each category CV-AVG: {}({}%) {}({}%) {}({}%) {}({}%)".format(hor, int(hor*100/hor_avg),
            #                                                                          vert, int(vert*100/vert_avg),
            #                                                                          diag45, int(diag45*100/diag45_avg),
            #                                                                          diag135, int(diag135*100/diag135_avg)))

            # Create new VMP file
            OUTNAME = os.path.join(PATH_CV, '{}_{}_avg_cv_vox_{}_{}{}.vmp'.format(su, fu, roi, tag, mask_suffix))
            avg_cv_vox = np.zeros(np.asarray(data_avg.shape))

            avg_cv_vox[idx_avg, 1] = CV_AVG_VOX                # labels
            new_idx = avg_cv_vox[..., 1] > 0

            avg_cv_vox[..., 0] = data_avg[..., 0] * new_idx    # t-value
            avg_cv_vox[..., 2] = data_avg[..., 2] * new_idx    # sensitivity
            avg_cv_vox[..., 3] = data_avg[..., 3] * new_idx    # specificity

            new_vmp_header = copy(header_avg)

            # Winner map
            new_vmp_header["Map"][1]["MapName"] = "CV-AVG Winner Map"
            new_vmp_header["Map"][1]["NrOfUsedVoxels"] = n_cv_avg

            new_vmp_header["Map"][0]["NrOfUsedVoxels"] =  n_cv_avg
            new_vmp_header["Map"][2]["NrOfUsedVoxels"] =  n_cv_avg
            new_vmp_header["Map"][3]["NrOfUsedVoxels"] =  n_cv_avg

            bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, avg_cv_vox)

            # Save dictionary to compute "confusion matrix", "consistency"
            CV_STEP2_DICT = {"SubjID": su, "contrast": fu,
                             "Labels_CV": CV_VOX, "Labels_AVG": AVG_VOX,
                             "Labels_CV_AVG": CV_AVG_VOX, "cv_vs_avg": idx_cv_avg,
                             "n_cv_avg": n_cv_avg, "n_cv_avg_cat": np.array([hor, vert,diag45, diag135]),
                             "n_avg_cat": np.array([hor_avg, vert_avg, diag45_avg, diag135_avg]),
                             "idx_AVG_3D": idx_avg}

            np.save(os.path.join(PATH_CV, "{}_{}_{}_{}{}_cv_step2_dict".format(su, fu, roi, tag, mask_suffix)),
                    CV_STEP2_DICT, allow_pickle=True)
            # ----------------------------------------------------------------
print("Done.")
