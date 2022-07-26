"""
Created on Tue Oct  5 14:07:15 2021
Vaso voxels investigation: BOLDmask coverage

@author: apizz
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import bvbabel
from copy import copy
from skimage.measure import label


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["VASO_interp_LN"]
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']
tag = 'c_thr_4'

VASO_BOLD_MASK = True
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')

for i, su in enumerate(SUBJ):
    PATH_AVG = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'GLM', 'ROI')
    FILE_AVG_B = '{}_{}_meanRuns_{}_ROI_{}_c_thr_4_BOLDMASK_preference_metrics.vmp'.format(su, FUNC[0], CONDT[0], ROI_NAME[0])
    FILE_AVG = '{}_{}_meanRuns_{}_ROI_{}_c_thr_4_preference_metrics.vmp'.format(su, FUNC[0], CONDT[0], ROI_NAME[0])

    # Q1: Does BOLD mask contain VASO significant voxels?
    header_BAVG, data_BAVG = bvbabel.vmp.read_vmp(os.path.join(PATH_AVG, FILE_AVG_B))
    header_AVG, data_AVG = bvbabel.vmp.read_vmp(os.path.join(PATH_AVG, FILE_AVG))

    idx_AVG = data_AVG[..., 1] > 0

    BAVG = data_BAVG[idx_AVG, 1]
    miss_vox_VASO = (BAVG == 0).astype(int)
    n_AVG = len(BAVG)
    n_BAVG = np.sum(BAVG > 0)

    data = np.zeros(np.asarray(data_AVG.shape[0:3]))
    data[idx_AVG] = miss_vox_VASO
    print("For {}, BOLD MASK covers {:.1f} ({}/{})".format(su, (n_BAVG / n_AVG) * 100, n_AVG, n_BAVG))

    # Q2: Are missing VASO voxels patched?
    # Connected Cluster Thresholding
    conn = 1
    c_thr = 4
    orig = copy(data)
    print("Original n of Voxels: {}".format(np.sum(orig)))
    data = np.where(data <= 0, 0, 1)

    data = label(data, connectivity=conn)
    labels, counts = np.unique(data, return_counts=True)
    print('{} clusters are found.'.format(labels.size))

    print('Applying connected clusters threshold (' + str(c_thr) + ' voxels).')
    for i, (i_label, i_count) in enumerate(zip(labels[1:], counts[1:])):
        if i_count < c_thr:
            data[data == i_label] = 0
    data[data != 0] = 1

    # Bring back the data
    x = orig[..., 1]
    n_vox = np.sum(orig[..., 1] >0)
    orig[data == 0] = 0
    print("Survivig Voxels: {}".format(np.sum(orig)))

    # Q3: Are cross-validated voxels (before thresholding with 2round of connected cluster)?
    if np.sum(orig) > 0:
        PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'cross_validation', 'Results')
        FILE_CV = "{}_{}_{}_c_thr_4_cv_step2_dict.npy".format(su, FUNC[0], ROI_NAME[0])
        idx_miss = orig > 0
        cv_dict = np.load(os.path.join(PATH_CV, FILE_CV), allow_pickle=True).item()

        mask_cv = cv_dict["idx_AVG_3D"].astype(int)
        x = mask_cv[orig > 0]
        orig[idx_miss] += x                   # label 2
        print("For {}, ({}/{}) are cross-validated".format(su, np.sum(orig>0), np.sum(x)))

        # Q3: Do they survive at stage CV-2?
        if np.sum(x) > 0:
            mask_cv2 = cv_dict["idx_cv_avg_c_thr"].astype(int)
            y = mask_cv2[orig > 0]
            orig[idx_miss] += y                   # label 3
            print("For {}, ({}/{}/{}) are cross-validated (c_thr)".format(su, np.sum(orig>0), np.sum(x), np.sum(y)))
            print("For {}, Vox lab 1(no cv): {}, Vox lab 2(cv step1): {}, Vox lab 3(cv step2): {}".format(su, np.sum(orig == 1), np.sum(orig == 2), np.sum(orig == 3)))

        # Export VMP
        new_vmp_data = np.concatenate((data_AVG, orig[..., None]), axis=3)

        # VMP preparation
        new_vmp_header = copy(header_AVG)
        new_vmp_header['NrOfSubMaps'] += 1
        new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))

        new_vmp_header["Map"][-1]["MapName"] = "VASO voxels missed in BOLDmask"
        new_vmp_header["Map"][-1]["NrOfUsedVoxels"] = np.sum(orig > 0, dtype=np.int32)
        new_vmp_header["Map"][-1]["EnableClusterSizeThreshold"] = 0
        new_vmp_header["Map"][-1]["ShowPosNegValues"] = 1
        new_vmp_header["Map"][-1]["UpperThreshold"] = 4
        new_vmp_header["Map"][-1]["MapThreshold"] = 1
        new_vmp_header["Map"][-1]["LUTFileName"] = "eccentricity_v1.olt"

        OUTNAME = os.path.join(PATH_AVG, "Missing_VASO_voxels_from_BOLDmask.vmp")
        bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
