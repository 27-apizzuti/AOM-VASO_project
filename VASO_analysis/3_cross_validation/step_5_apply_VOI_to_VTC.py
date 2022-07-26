""" Apply ROI to vtc file before computing GLM for Cross-Validation.
    The ROI considered here is 'bilateral MT' comes from Localizer.
    (no hemisphere difference is condered)

    NB: ROI indices are referred to VMR file (256, 256, 256) instead VTC data
    does not (it has original nifiti dimensions)
    The 2 files overlap thanks to VTC header info.

This step is needed because BV ROI-GLM python function doesn't work.

Updated on Wed Sep 29 2021

@author: apizz
"""

import os
import bvbabel
import numpy as np
from copy import copy
from glob import glob

print("Hello!")

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
#SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
SUBJ = ["sub-07"]
CONTR = ["BOLD_interp", "VASO_interp_LN"]
PROC = 'standard'
ROI_NAME = 'conj_bilMT_anat_sphere16radius'

# =============================================================================
for iterSbj in SUBJ:
    PATH_IN = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', PROC, 'cross_validation')
    FLD_IN = glob(os.path.join(PATH_IN, "run*", ""))
    for iterFLD in FLD_IN:
        for iterContrast in CONTR:
            print("Working on {} {} CV {}".format(iterSbj, iterContrast, iterFLD))

            # Read VTC
            PATH_VTC = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', PROC, 'cross_validation', iterFLD, 'GLM')
            FILE_VTC = os.path.join(PATH_VTC, '{}_bvbabel.vtc'.format(iterContrast))
            header, data = bvbabel.vtc.read_vtc(FILE_VTC)

            # Read VOI directly
            PATH_VOI = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'loc01',
                                        'BV_GLM')
            FILENAME_VOI = '{}_{}.voi'.format(iterSbj, ROI_NAME)
            PATH_VOI = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'loc01',
                                    'BV_GLM')
            header_voi, data_voi = bvbabel.voi.read_voi(os.path.join(PATH_VOI, FILENAME_VOI))

            coords = copy(data_voi[0]["Coordinates"])

            # Find indices inside VTC range (VOI can be bigger)
            idx_x = (coords[:, 0] >= header["XStart"]) * (coords[:, 0] < header["XEnd"])
            idx_y = (coords[:, 1] >= header["YStart"]) * (coords[:, 1] < header["YEnd"])
            idx_z = (coords[:, 2] >= header["ZStart"]) * (coords[:, 2] < header["ZEnd"])

            idx = idx_x * idx_y * idx_z
            coords_vtc_voi = coords[idx, :]

            # Apply transformation (translation)
            coords_vtc_voi[:, 0] -= header["XStart"]
            coords_vtc_voi[:, 1] -= header["YStart"]
            coords_vtc_voi[:, 2] -= header["ZStart"]

            x = coords_vtc_voi[:, 2]
            y = coords_vtc_voi[:, 0]
            z = coords_vtc_voi[:, 1]

            # Initialize new VMP matrix
            mask_vmp_voi = np.zeros(data.shape)
            mask_vmp_voi[x, y, z, :] = 1

            # Masking original VMP with ROI
            new_vmp_voi = mask_vmp_voi[::-1, ::-1, ::-1, :]
            data *= new_vmp_voi

            # Save new VTC
            basename = FILE_VTC.split(os.extsep, 1)[0]
            OUTNAME = "{}_bvbabel_masked_VOI_{}.vtc".format(basename, ROI_NAME)
            bvbabel.vtc.write_vtc(OUTNAME, header, data)

print("Done.")
