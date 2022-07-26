"""
Leave one run out Cross-Validation
Step_1: Voxel selection within folds based on train vs test label agreement

STEPS:
    1) Select Training Voxels (vox_idx): vox_t_value > q_fdr (q=0.05)
    2) Compute Winner Maps for Training (vox_idx) -> vox_label_train
    3) Compute Winner Maps for Test (vox_idx) -> vox_label_test
    4) Compare Training Vs Test Labels-vox_label_cv_step1
    5) Save .npz dictionary

Spanning across all Cross-Validation subfolders
    INPUT: VMP
    OUTPUT: VMP and .npy in "Cross-Validation/Results"

NOTE:
    Maps oder in .vmp: 1) Horizontal, 2) Vertical 3) Diag45 4) Diag135 5) All Conditions
    Multiple subjects possible
    Run separately for each roi (e.g. 'left', 'right')

Created on Wed Sep 15 17:04:12 2021
@author: apizz
"""

import os
import numpy as np
import bvbabel
from glob import glob
from copy import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']                                       # Always put BOLD first, "VASO"
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']

for su in SUBJ:
    PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'cross_validation')
    PATH_OUT = os.path.join(PATH_CV, 'Results')

    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
    for roi in ROI_NAME:

        for fu in FUNC:
            print("Processing {} {}".format(fu, su))
            CV_VOX_LABEL = []; STATS_CV = [];                                      # // initializing output variables
            STATS_TRAIN = []; STATS_TEST = [];
            CVFLD = glob(os.path.join(PATH_CV, "runs*", ""))
            runs = np.linspace(0, len(CVFLD)-1, len(CVFLD), dtype='int8')

            for cv in CVFLD:
                PATH_VMP_TRAIN = os.path.join(PATH_CV, cv, 'GLM', 'ROI')
                FILENAME_VMP = '{}_{}_meanRuns_{}_ROI_{}.vmp'.format(su, fu, CONDT[0], roi)

                train_runs = cv.split('\\')[-2]
                train_runs = np.asarray(train_runs.split("_")[1:], dtype='int8')
                test_run = np.setdiff1d(runs, train_runs)                          # // to find left-out run

                PATH_VMP_TEST = os.path.join(PATH_CV, 'run_{}'.format(str(test_run[0])), 'GLM', 'ROI')

                print('training: {}, test: {}'.format(train_runs, test_run))

                # Read VMP Training & Test
                IN_FILE_TRAIN = os.path.join(PATH_VMP_TRAIN, FILENAME_VMP)
                header_train, data_train = bvbabel.vmp.read_vmp(IN_FILE_TRAIN)

                IN_FILE_TEST = os.path.join(PATH_VMP_TEST, FILENAME_VMP)
                header_test, data_test = bvbabel.vmp.read_vmp(IN_FILE_TEST)
                n_maps = header_train['NrOfSubMaps']

                # Only a set of voxels if found by data_train
                if fu == "VASO_interp_LN":
                    data_train *= -1        # flip VASO sign
                    data_test *= -1

                vox_idx = data_train[:, :, :, 4] > 0                  # // considering all voxels indices [no FDR thresholding]

                # Create 4D matrix of significant t-values
                temp_train = np.zeros(data_train.shape[0:3] + (4,))                # // 4D matrices, last dim is the contrast
                temp_test = np.zeros(data_train.shape[0:3] + (4,))

                # Get t-value for Training and Test (put together all the 3D maps)
                for iterCond in range(0, 4):
                    temp_train[vox_idx, iterCond] = data_train[vox_idx, iterCond]
                    temp_test[vox_idx, iterCond] = data_test[vox_idx, iterCond]

                # Get values of the significant voxels
                vox_tvalue_train = temp_train[vox_idx, :]                          # // 2D matrix of t-values, [voxels x contrast]
                vox_tvalue_test = temp_test[vox_idx, :]

                # Compute Winner/Preference Map
                vox_label_train = np.zeros(len(vox_tvalue_train))              # // 1D vector of indices of the max
                vox_label_test = np.zeros(len(vox_tvalue_test))
                for it in range(0, len(vox_tvalue_train)):
                    if np.all(vox_tvalue_train[it, :] == vox_tvalue_train[it, 0]):
                        vox_label_train[it] = 0
                    else:
                        vox_label_train[it] = np.argmax(vox_tvalue_train[it, :]) + 1  # // +1 added because labels starts with 1
                    if np.all(vox_tvalue_test[it, :] == vox_tvalue_test[it, 0]):
                        vox_label_test[it] = 0
                    else:
                        vox_label_test[it] = np.argmax(vox_tvalue_test[it, :]) + 1

                # STEP 1: Compare training and test labels
                temp = np.zeros(vox_label_train.shape)                             # // initilize 1D vector
                vox_label_step1 = np.zeros(data_train.shape[0:3])                  # // initialize 3D matrix

                idx_step1 = vox_label_train == vox_label_test                      # // common voxels (1D boolean)
                temp[idx_step1] = vox_label_train[idx_step1]                       # // fill 1D vector with labels
                vox_label_step1[vox_idx] = temp                                    # // put 1D voxel's labels into 3D matrix

                # To check --------------------------------------------------------
                # Add 3 maps to the training VMP file
                temp_train_label = np.zeros(data_train.shape[0:3])
                temp_train_label[vox_idx] = vox_label_train

                temp_test_label = np.zeros(data_test.shape[0:3])
                temp_test_label[vox_idx] = vox_label_test

                OUTNAME = os.path.join(PATH_VMP_TRAIN, '{}_{}_check_cv_vox.vmp'.format(fu, roi))
                new_vmp_data = np.concatenate((data_train, vox_label_step1[..., None],
                                              temp_train_label[..., None], temp_test_label[..., None]), axis=3)
                new_vmp_header = copy(header_train)
                new_vmp_header['NrOfSubMaps'] += 3
                new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
                new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
                new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))

                # 1) Winner map (common voxels btw training and test)
                new_vmp_header["Map"][6]["MapName"] = "CV Training_Test Winner Map"
                new_vmp_header["Map"][6]["NrOfUsedVoxels"] = np.sum(idx_step1)
                new_vmp_header["Map"][6]["EnableClusterSizeThreshold"] = 0
                new_vmp_header["Map"][6]["ShowPosNegValues"] = 1
                new_vmp_header["Map"][6]["UpperThreshold"] = np.max(vox_label_step1)
                new_vmp_header["Map"][6]["MapThreshold"] = 1
                new_vmp_header["Map"][6]["LUTFileName"] = "eccentricity_v1.olt"

                # 2) Training Labels
                new_vmp_header["Map"][7]["MapName"] = "Training Winner Map"
                new_vmp_header["Map"][7]["NrOfUsedVoxels"] = np.sum(idx_step1)
                new_vmp_header["Map"][7]["EnableClusterSizeThreshold"] = 0
                new_vmp_header["Map"][7]["ShowPosNegValues"] = 1
                new_vmp_header["Map"][7]["UpperThreshold"] = np.max(vox_label_step1)
                new_vmp_header["Map"][7]["MapThreshold"] = 1
                new_vmp_header["Map"][7]["LUTFileName"] = "eccentricity_v1.olt"

                # 3) Test Labels
                new_vmp_header["Map"][8]["MapName"] = "Test Winner Map"
                new_vmp_header["Map"][8]["NrOfUsedVoxels"] = np.sum(idx_step1)
                new_vmp_header["Map"][8]["EnableClusterSizeThreshold"] = 0
                new_vmp_header["Map"][8]["ShowPosNegValues"] = 1
                new_vmp_header["Map"][8]["UpperThreshold"] = np.max(vox_label_step1)
                new_vmp_header["Map"][8]["MapThreshold"] = 1
                new_vmp_header["Map"][8]["LUTFileName"] = "eccentricity_v1.olt"

                bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
                # ----------------------------------------------------------------

                # Statistics
                train_info = []; test_info = []; cv_s1_info = [];
                for it in [1, 2, 3, 4]:
                    train_info.append(np.count_nonzero(vox_label_train == it))
                    test_info.append(np.count_nonzero(vox_label_test == it))
                    cv_s1_info.append(np.count_nonzero(temp == it))
                train_info.append(len(vox_label_train))
                test_info.append(len(vox_label_test)); cv_s1_info.append(np.sum(cv_s1_info));

                CV_VOX_LABEL.append(vox_label_step1); STATS_CV.append(cv_s1_info);
                STATS_TRAIN.append(train_info); STATS_TEST.append(test_info);

            coords_x = [header_train["XStart"], header_train["XEnd"]]
            coords_y = [header_train["YStart"], header_train["YEnd"]]
            coords_z = [header_train["ZStart"], header_train["ZEnd"]]

            CV_STEP1_DICT = {"SubjID": su, "n_folds": len(runs), "order_folds": CVFLD, "contrast": fu,
                             "Labels": CV_VOX_LABEL, "Stats_cv": STATS_CV,
                            "Stats_Train": STATS_TRAIN, "Stats_Test": STATS_TEST,
                            "X_range": coords_x, "Y_range": coords_y, "Z_range": coords_z}

            np.save(os.path.join(PATH_OUT, "{}_{}_{}_cv_step1_dict".format(su, fu, roi)),
                    CV_STEP1_DICT, allow_pickle=True)

print("Done.")
