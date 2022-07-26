"""
Created on Tue Oct  5 20:41:25 2021

Comparing BOLD and VASO
CV-AVG set of voxels

VASO: BOLDmask

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
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')

for roi in ROI_NAME:
    my_dpi = 96
    cols = len(SUBJ)
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

    # Set of indices we want to evaluate
    BOLD_vox = []
    VASO_vox = []
    COMM_vox = []

    CV_BOLD = []
    CV_VASO = []
    BOLD_FDR = []

    for i, su in enumerate(SUBJ):
        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'cross_validation', 'Results')
        FILE_V = "{}_VASO_interp_LN_avg_cv_vox_{}_c_thr_4_BOLDMASK_c_thr_4.vmp".format(su, roi)
        FILE_B = "{}_BOLD_interp_avg_cv_vox_{}_c_thr_4_c_thr_4.vmp".format(su, roi)

        FILE_BOLDmask = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI', '{}_BOLD_interp_meanRuns_standard_ROI_{}_c_thr_4.vmp'.format(su, roi))

        header_B, data_B = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_B))
        header_V, data_V = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_V))

        header_Bmask, data_Bmask = bvbabel.vmp.read_vmp(FILE_BOLDmask)

        # BOLDmask indices
        idxBOLDmask = data_Bmask[..., 6] > 0

        B_flat = data_B[..., 1].flatten()
        V_flat = data_V[..., 1].flatten()

        SenB_flat = data_B[..., 2].flatten()
        SenV_flat = data_V[..., 2].flatten()

        SpecB_flat = data_B[..., 3].flatten()
        SpecV_flat = data_V[..., 3].flatten()

        # Q1: Spatial displacement?
        idxB = B_flat > 0
        idxV = V_flat > 0

        CV_BOLD.append(np.reshape(idxB, [162, 216, 26]))
        CV_VASO.append(np.reshape(idxV, [162, 216, 26]))
        BOLD_FDR.append(idxBOLDmask)

        idx_common = idxB * idxV
        print("For {}, BOLD vox: {}, VASO vox: {}, common voxels: {}".format(su, np.sum(idxB > 0),
                                                                                      np.sum(idxV > 0), np.sum(idx_common)))
        # Q2: Common voxels show the same label between BOLD and VASO?
        l_B = B_flat[idx_common]
        l_V = V_flat[idx_common]

        lab_common = (l_B == l_V)                              # common labels
        vox_bold = (idx_common == False) * idxB
        vox_vaso = (idx_common == False) * idxV

        # Put back indices of common labels
        idx_common_best = (B_flat == V_flat) * idx_common

        # We have 3 groups now: only BOLD, only VASO, common voxels
        print("For {}, common vox: {}, shared labels: {}".format(su, np.sum(idx_common), np.sum(lab_common > 0)))

        # 1) Functional behavior: balanced classes?
        for it in range(1, 5):
            if np.sum(l_B[lab_common] == it) > 0:
                print("For {} label {}, bold: {:.1f}%, vaso: {:.1f}%, common: {:.1f}%".format(su, it,
                      (np.sum(B_flat[vox_bold] == it)/np.sum(B_flat[vox_bold] > 0)) * 100,
                      (np.sum(V_flat[vox_vaso] == it)/np.sum(V_flat[vox_vaso] > 0)) * 100,
                      (np.sum(l_B[lab_common] == it)/np.sum(lab_common > 0)) *100))
            else:
                print("For {} label {}, bold: {:.1f}%, vaso: {:.1f}%, no common".format(su, it,
                      np.sum(B_flat[vox_bold] == it)/np.sum(B_flat[vox_bold] > 0) * 100,
                      np.sum(V_flat[vox_vaso] == it)/np.sum(V_flat[vox_vaso] > 0) * 100))

        # 2) Specificity and sensitivity
        centroids = np.matrix([[np.mean(SenB_flat[vox_bold]), np.mean(SpecB_flat[vox_bold])],
                               [np.mean(SenV_flat[vox_vaso]), np.mean(SpecV_flat[vox_vaso])],
                               [np.mean(SenV_flat[idx_common]), np.mean(SpecV_flat[idx_common])],
                               [np.mean(SenB_flat[idx_common]), np.mean(SpecB_flat[idx_common])]])

        print("For {}, BOLD Sen,Spec: {:.1f}, {:.1f}".format(su, centroids[0, 0], centroids[0, 1]))
        print("For {}, VASO Sen,Spec: {:.1f}, {:.1f}".format(su, centroids[1, 0], centroids[1, 1]))
        print("For {}, Common Sen,Spec: {:.1f}, {:.1f}".format(su, centroids[2, 0], centroids[2, 1]))
        # ---------------------------------------------------------------------
        # 4Groups-Scatterplot
        # Plotting
        axs[0].scatter(SenB_flat[vox_bold],
                          SpecB_flat[vox_bold],
                          color='black',
                          alpha=0.2)
        axs[0].scatter(centroids[0, 0], centroids[0, 1],
                       marker = "x", linewidths = 4, color='black')

        axs[0].scatter(SenB_flat[idx_common_best],
                          SpecB_flat[idx_common_best],
                          color='red',
                          alpha=0.2)
        axs[0].scatter(centroids[3, 0], centroids[3, 1],
                       marker = "x", linewidths = 4, color='red')

        axs[0].set_ylabel("Specificity (1-div)")
        axs[0].set_xlabel("Sensitivity (L2norm)")
        axs[0].set_ylim([0, 1])
        axs[0].set_xlim([0, 30])
        axs[0].grid("True")
        axs[0].set_title("BOLD vox and best BOLD vox")
        # -------------------------------------

        axs[1].scatter(SenV_flat[vox_vaso],
                          SpecV_flat[vox_vaso],
                          color='black',
                          alpha=0.2)
        axs[1].scatter(centroids[1, 0], centroids[1, 1],
                       marker = "x", linewidths = 3, color='black')

        axs[1].scatter(SenV_flat[idx_common_best],
                          SpecV_flat[idx_common_best],
                          color='red',
                          alpha=0.2)

        axs[1].scatter(centroids[2, 0], centroids[2, 1],
                       marker = "x", linewidths = 3, color='red')

        axs[1].set_ylabel("Specificity (1-div)")
        axs[1].set_xlabel("Sensitivity (L2norm)")
        axs[1].set_ylim([0, 1])
        axs[1].set_xlim([0, 30])
        axs[1].grid("True")
        axs[1].set_title("VASO vox and best VASO vox")
        #plt.suptitle("CV-AVG Voxel's Characterization {} \n\n\n".format(roi))
        BOLD_vox.append(np.reshape(vox_bold, [162, 216, 26]))
        VASO_vox.append(np.reshape(vox_vaso, [162, 216, 26]))
        COMM_vox.append(np.reshape(idx_common_best, [162, 216, 26]))

    fig_filename = "three_groups_scatterplot_{}".format(roi)
    fig.tight_layout()
    plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
    plt.show()
    #4 euSNN progress report ---------------------------------------------------------------------
#         axs[0].scatter(SenB_flat[vox_bold],
#                           SpecB_flat[vox_bold],
#                           color='black',
#                           alpha=0.2)
#         #axs[0].scatter(centroids[0, 0], centroids[0, 1],
# #                       marker = "x", linewidths = 4, color='black')
#
#         axs[0].scatter(SenB_flat[idx_common_best],
#                           SpecB_flat[idx_common_best],
#                           color='black',
#                           alpha=0.2)
#         #axs[0].scatter(centroids[3, 0], centroids[3, 1],
# #                       marker = "x", linewidths = 4, color='red')
#
#         axs[0].set_ylabel("Specificity (1-div)")
#         axs[0].set_xlabel("Sensitivity (L2norm)")
#         axs[0].set_ylim([0, 1])
#         axs[0].set_xlim([0, 30])
#         axs[0].grid("True")
#         axs[0].set_title("Cross-validated BOLD voxels")
#         # -------------------------------------
#
#         axs[1].scatter(SenV_flat[vox_vaso],
#                           SpecV_flat[vox_vaso],
#                           color='black',
#                           alpha=0.2)
#         # axs[1].scatter(centroids[1, 0], centroids[1, 1],
#         #                marker = "x", linewidths = 3, color='black')
#
#         axs[1].scatter(SenV_flat[idx_common_best],
#                           SpecV_flat[idx_common_best],
#                           color='black',
#                           alpha=0.2)
#
#         # axs[1].scatter(centroids[2, 0], centroids[2, 1],
#         #                marker = "x", linewidths = 3, color='red')
#
#         axs[1].set_ylabel("Specificity (1-div)")
#         axs[1].set_xlabel("Sensitivity (L2norm)")
#         axs[1].set_ylim([0, 1])
#         axs[1].set_xlim([0, 30])
#         axs[1].grid("True")
#         axs[1].set_title("Cross-validated VASO voxels")
#         #plt.suptitle("CV-AVG Voxel's Characterization {} \n\n\n".format(roi))
#         BOLD_vox.append(np.reshape(vox_bold, [162, 216, 26]))
#         VASO_vox.append(np.reshape(vox_vaso, [162, 216, 26]))
#         COMM_vox.append(np.reshape(idx_common_best, [162, 216, 26]))
#
#     fig_filename = "4eusnn_report_{}".format(roi)
#     fig.tight_layout()
#     plt.savefig(os.path.join(PATH_OUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
#     plt.show()
    GROUP_DICT = {"BOLD_vox": BOLD_vox, "VASO_vox": VASO_vox,
                              "COMM_vox": COMM_vox, "CV_BOLD": CV_BOLD, "CV_VASO": CV_VASO, "BOLD_FDR": BOLD_FDR}
    np.save(os.path.join(PATH_OUT, "Group_idices_BOLD_VASO_COMM_CV_BOLDfdr_{}".format(roi)),
                    GROUP_DICT, allow_pickle=True)
