"""
Created on Tue Jul 27 20:01:40 2021
Updated on Wed Sep 29 2021

    Apply VOI to a VMP

    1. Read VOI and VMP_data
    2. Convert VOI into VMP_from_VOI using bvbabel
    3. Mask VMP_data using VMP_from_VOI
    4. Save VMP_data adding VMP_from_VOI as last map
    (no bvbabel version reliase available yet-0.0.2)

INPUT:  - VOI (e.g. rightMT_Sphere16radius.voi)
        - VMP_data (e.g. BOLD_meanRuns_noNORDIC_ROI.vmp)
OUTPUT:
        - new VMP_data (saved in the same VMP_data folder)

@author: apizz
"""
import os
import numpy as np
import bvbabel
from copy import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07"]
CONDT = ["standard"]
FUNC = ["BOLD_interp", "VASO_interp_LN"]
ROI_NAME = ["leftMT_Sphere16radius", "rightMT_Sphere16radius"]

# ===========================Execute========================================
for su in SUBJ:

    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'GLM', 'ROI')

    PATH_VOI = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'loc01',
                                    'BV_GLM')

    for fu in FUNC:

        FILENAME_VMP = '{}_{}_meanRuns_{}_ROI.vmp'.format(su, fu, CONDT[0])

        for roi in ROI_NAME:
            print("Processing {} {} with {}".format(fu, su, roi))

            FILENAME_VOI = '{}_{}.voi'.format(su, roi)

            # Read VMP
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data = bvbabel.vmp.read_vmp(IN_FILE)

            # Read VOIs
            header_voi, data_voi = bvbabel.voi.read_voi(os.path.join(PATH_VOI, FILENAME_VOI))
            coords = copy(data_voi[0]["Coordinates"])

            # ------------------------------------------------------------------------
            # BE CAREFUL on this line because bvbabel might change

            # Find indices inside VMP range (VOI can be bigger)
            idx_x = (coords[:, 0] >= header["XStart"]) * (coords[:, 0] < header["XEnd"])
            idx_y = (coords[:, 1] >= header["YStart"]) * (coords[:, 1] < header["YEnd"])
            idx_z = (coords[:, 2] >= header["ZStart"]) * (coords[:, 2] < header["ZEnd"])

            idx = idx_x * idx_y * idx_z
            coords_vmp_voi = coords[idx, :]

            # Apply transformation (translation)
            coords_vmp_voi[:, 0] -= header["XStart"]
            coords_vmp_voi[:, 1] -= header["YStart"]
            coords_vmp_voi[:, 2] -= header["ZStart"]

            x = coords_vmp_voi[:, 2]
            y = coords_vmp_voi[:, 0]
            z = coords_vmp_voi[:, 1]

            # Initialize new VMP matrix
            mask_vmp_voi = np.zeros(data.shape)
            mask_vmp_voi[x, y, z, :] = 1

            # Masking original VMP with ROI
            new_vmp_voi = mask_vmp_voi[::-1, ::-1, ::-1, :]
            data *= new_vmp_voi

            # ===========================================================================
            # Add VOI as last map of the VMP (as check point)
            voi_map = new_vmp_voi[..., 0]
            new_vmp_data = np.concatenate((data, voi_map[..., None]), axis=3)

            # VMP preparation
            new_vmp_header = copy(header)
            new_vmp_header['NrOfSubMaps'] += 1
            new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))

            new_vmp_header["Map"][-1]["MapName"] = data_voi[0]["NameOfVOI"]
            new_vmp_header["Map"][-1]["NrOfUsedVoxels"] = np.sum(new_vmp_data, dtype=np.int32)
            new_vmp_header["Map"][-1]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][-1]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][-1]["UpperThreshold"] = np.max(new_vmp_data)
            new_vmp_header["Map"][-1]["MapThreshold"] = np.min(new_vmp_data)

            # Export VMP
            basename = IN_FILE.split(os.extsep, 1)[0]
            OUTNAME = "{}_{}.vmp".format(basename, roi)
            bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)

print("Done.")
