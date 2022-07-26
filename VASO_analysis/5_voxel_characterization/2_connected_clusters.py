"""
Created on Fri Oct  1 15:08:34 2021
Connected clusters cluster size thresholding for VMP maps

adapted from: https://gist.github.com/ofgulban/27c4491592126dce37e97c578cbf307b
@author: apizz
"""

import os
import numpy as np
import bvbabel
from copy import copy
from skimage.measure import label

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07"]
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["leftMT_Sphere16radius", "rightMT_Sphere16radius"]

for su in SUBJ:
    # Read VMP
    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'GLM', 'ROI')
    for roi in ROI_NAME:
        for fu in FUNC:
            print("Working on {} {} {}".format(su, fu, roi))
            FILENAME_VMP = "{}_{}_meanRuns_{}_ROI_{}.vmp".format(su, fu, CONDT[0], roi)
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data_vmp = bvbabel.vmp.read_vmp(IN_FILE)

            # Extract FDR threshold from Map #5
            q = 0.05
            pos = np.round(header['Map'][4]['FDRTableInfo'][:, 0], decimals=3, out=None) == q
            fdr_thres = header['Map'][4]['FDRTableInfo'][pos, 1]

            # Parameters
            thr = fdr_thres
            c_thr = 0
            conn = 1

            # ========== Execute
            print('Data will be intensity thresholded ({}).'.format(thr))
            orig = copy(data_vmp)
            if fu == "VASO_interp_LN":
                data = -1 * data_vmp[..., 4]
            else:
                data = data_vmp[..., 4]
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
            x = orig[..., 4]
            x[data == 0] = 0

            # Export VMP
            new_vmp_data = np.concatenate((orig, x[..., None]), axis=3)

            # VMP preparation
            new_vmp_header = copy(header)
            new_vmp_header['NrOfSubMaps'] += 1
            new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))

            new_vmp_header["Map"][-1]["MapName"] = "Cluster sixe thresholded ({}): All Conds vs Flicker".format(c_thr)
            new_vmp_header["Map"][-1]["NrOfUsedVoxels"] = np.sum(data > 0, dtype=np.int32)
            new_vmp_header["Map"][-1]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][-1]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][-1]["UpperThreshold"] = new_vmp_header["Map"][4]["UpperThreshold"]
            new_vmp_header["Map"][-1]["MapThreshold"] = new_vmp_header["Map"][4]["MapThreshold"]

            basename = IN_FILE.split(os.extsep, 1)[0]
            OUTNAME = "{}_c_thr_{}.vmp".format(basename, c_thr)
            bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
