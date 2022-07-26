"""
Created on Fri Oct  1 15:08:34 2021
Connected clusters cluster size thresholding for VMP maps

Update npy dict 2 with indices of CV-Voxels survived to this step.

adapted from: https://gist.github.com/ofgulban/27c4491592126dce37e97c578cbf307b
@author: apizz
"""

import os
import numpy as np
import bvbabel
from copy import copy
from skimage.measure import label

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["leftMT_Sphere16radius", "rightMT_Sphere16radius"]
tag = 'c_thr_4'
VASO_BOLD_MASK = False

# Parameters
thr = 0
c_thr = 4
conn = 1

for su in SUBJ:
    # Read VMP
    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'cross_validation', 'Results')
    for roi in ROI_NAME:
        for fu in FUNC:
            print("Working on {} {} {}".format(su, fu, roi))

            mask_suffix = ""
            if fu == "VASO_interp_LN" and VASO_BOLD_MASK:
                mask_suffix = "_BOLDMASK"
            FILENAME_VMP = "{}_{}_avg_cv_vox_{}_{}{}.vmp".format(su, fu, roi, tag, mask_suffix)
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data_vmp = bvbabel.vmp.read_vmp(IN_FILE)

            # Read dictionary step 2 to add new indices after cluster thresholding
            NPZ_CV = "{}_{}_{}_{}{}_cv_step2_dict.npy".format(su, fu, roi, tag, mask_suffix)

            cv_avg_dict = np.load(os.path.join(PATH_VMP, NPZ_CV),
                                          allow_pickle=True).item()

            # ========== Execute
            print('Data will be intensity thresholded ({}).'.format(thr))
            orig = copy(data_vmp)
            data = data_vmp[..., 1]

            data = np.where(data <= thr, 0, 1)

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
            x[data == 0] = 0

            print("{} {} {} N voxels: {}({}%)".format(su, roi, fu, np.sum(x > 0),
                                                      int(np.sum(x > 0)*100/n_vox) ))

            # Extract 3D bool indices of CV AVG voxels
            idx = x > 0
            cv_avg_dict["idx_cv_avg_c_thr"] = idx
            cv_avg_dict["nVOX_cv_avg_c_thr"] = [np.sum(x > 0), int(np.sum(x > 0)*100/n_vox)]

            # Save updated dictionary
            np.save(os.path.join(PATH_VMP, NPZ_CV),
                    cv_avg_dict, allow_pickle=True)

            # Export VMP
            new_vmp_data = np.concatenate((orig, x[..., None]), axis=3)

            # VMP preparation
            new_vmp_header = copy(header)
            new_vmp_header['NrOfSubMaps'] += 1
            new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))

            new_vmp_header["Map"][-1]["MapName"] = "Cluster sixe thresholded ({}): CV AVG vox".format(c_thr)
            new_vmp_header["Map"][-1]["NrOfUsedVoxels"] = np.sum(data > 0, dtype=np.int32)
            new_vmp_header["Map"][-1]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][-1]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][-1]["UpperThreshold"] = new_vmp_header["Map"][1]["UpperThreshold"]
            new_vmp_header["Map"][-1]["MapThreshold"] = new_vmp_header["Map"][1]["MapThreshold"]
            new_vmp_header["Map"][-1]["LUTFileName"] = "eccentricity_v1.olt"

            basename = IN_FILE.split(os.extsep, 1)[0]
            OUTNAME = "{}_c_thr_{}.vmp".format(basename, c_thr)
            bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
