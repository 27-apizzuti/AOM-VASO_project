"""
Leave one run out Cross-Validation
Step_3: Compute confusion matrix: CV AVG (after cluster thresholding) vs AVG
Created on Fri Sep 17 15:07:51 2021
@author: apizz
"""
import os
import numpy as np
from fnc_plot_confusion_matrix import *

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']
ROI_NAME = ['leftMT_Sphere16radius', 'rightMT_Sphere16radius']
tag = 'c_thr_4'
VASO_BOLD_MASK = True

for roi in ROI_NAME:
    for su in SUBJ:
        for fu in FUNC:

            PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', CONDT[0], 'cross_validation', 'Results')

            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"

            NPZ_CV = "{}_{}_{}_{}{}_cv_step2_dict.npy".format(su, fu, roi, tag, mask_suffix)

            cv_avg_dict = np.load(os.path.join(PATH_CV, NPZ_CV),
                                          allow_pickle=True).item()

            # Find discarded voxels from the cluster thresholding
            temp = cv_avg_dict["idx_AVG_3D"] == True
            idx = cv_avg_dict["idx_cv_avg_c_thr"]
            CV_AVG_C_THR = idx[temp>0]

            # ----------------------------------------
            AVG_VOX = cv_avg_dict["Labels_AVG"]      # * CV_AVG_C_THR
            CV_VOX = cv_avg_dict["Labels_CV"]

            PRED_VOX = np.zeros(len(AVG_VOX))
            for it in range(0, len(AVG_VOX)):
                if np.sum(CV_VOX[it, :]) > 0:
                    cond = CV_VOX[it, :] == AVG_VOX[it]
                    if np.sum(cond) > 0:        # // if one of CV folds shows the same label of AVG
                        PRED_VOX[it] = AVG_VOX[it]
                    else:
                        temp = np.zeros(4)      # // create an occurrence vector
                        for it1 in range(0, 4):
                            temp[it1] = np.count_nonzero(CV_VOX[it, :] == it1+1)
                        if np.sum(temp == temp.max()) == 1:    # // exist a unique occurrent label
                            idx = np.argmax(temp)
                            PRED_VOX[it] = idx +1              # // the voxel was mis-classified

            # Create 1D vector of predicted labels
            conf_matrix = np.zeros([4, 4])             # // predicted (col) & test (row)
            for itervox in range(0, len(AVG_VOX)):
                lab_avg = int(AVG_VOX[itervox])
                lab_pred = int(PRED_VOX[itervox])
                if lab_pred > 0:
                    conf_matrix[lab_avg-1, lab_pred-1] += 1

            # TPR and PPV
            TPR = np.diag(conf_matrix) / np.sum(conf_matrix, axis=1)
            PPV = np.diag(conf_matrix) / np.sum(conf_matrix, axis=0)

            # Plot confusion matrix
            my_dpi = 96
            y_true = AVG_VOX[PRED_VOX>0]
            y_pred = PRED_VOX[PRED_VOX>0]
            filename = os.path.join(PATH_CV, '{}_{}_{}_{}_confusion_matrix{}.png'.format(su, fu, roi, tag, mask_suffix))
            labels = [1, 2, 3, 4]
            cm_analysis(y_true, y_pred, filename, labels, ymap=None, figsize=(10, 10))

            # Plot Consistency
            filename_cons = os.path.join(PATH_CV, '{}_{}_{}_{}_consistency{}.png'.format(su, fu, roi, tag, mask_suffix))
            cons = cv_avg_dict["Labels_CV"] * CV_AVG_C_THR[..., None]

            temp = np.zeros([4, np.shape(cons)[1]])

            for it in range(0, len(cons)):
                if np.sum(cons[it, :]) > 0:
                    x = cons[it, :]
                    n = np.sum(x > 0)                  # ricorrenza
                    l = int(x[x > 0][0])               # label
                    temp[l-1, n-1] += 1

            if np.shape(cons)[1] == 4:
                labels = ['1/4', '2/4', '3/4', '4/4']
            else:
                labels = ['1/3', '2/3', '3/3']
            h = temp[0, :]
            v = temp[1, :]
            d1 = temp[2, :]
            d2 = temp[3, :]
            width = 0.35       # the width of the bars: can also be len(x) sequence

            fig, ax = plt.subplots()

            ax.bar(labels, h, width, label='Horizontal')
            ax.bar(labels, v, width, label='Vertical', bottom=h)
            ax.bar(labels, d1, width, label='Diagonal 45', bottom=np.array(h)+np.array(v))
            ax.bar(labels, d2, width, label='Diagonal 135', bottom=np.array(h)+np.array(v)+np.array(d1))

            ax.set_ylabel('N. Of Voxels per Motion Direction')
            ax.set_xlabel('Consistency')
            ax.legend()
            plt.savefig(filename_cons)
            plt.show()
            # Save dictionary "confusion matrix"
            CV_STEP3_DICT = {"SubjID": su, "contrast": fu,
                             "confusion_matrix": conf_matrix, "TPR" : TPR,
                             "PPV": PPV}
            np.save(os.path.join(PATH_CV, "{}_{}_{}_{}_cv_step3_dict{}".format(su, fu, roi, tag, mask_suffix)),
                    CV_STEP3_DICT, allow_pickle=True)
