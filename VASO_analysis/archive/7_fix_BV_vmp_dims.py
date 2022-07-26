"""
Created on Mon Sep 20 18:13:20 2021:
    TRY FIX VMP DIM of AVG files,
    bring it back from BV cut to its original dimension.

@author: apizz
"""

import os
import bvbabel
import nibabel as nib
import numpy as np
from copy import copy

print("Hello!")

# =============================================================================
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ =  ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONTR = ["BOLD", "VASO"]
PROC = 'standard'

for iterSbj in SUBJ:

    # Load nifti and VTC/VMP
    PATH_NII = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'boco')
    PATH_VMP = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'GLM', 'ROI')

    for iterContrast in CONTR:

        print('Working on {} contrast {}'.format(iterSbj, iterContrast))

        # Load VMP
        FILE_VMP = os.path.join(PATH_VMP, '{}_meanRuns_noNordic_ROI.vmp').format(iterContrast)
        header_vmp, data_vmp = bvbabel.vmp.read_vmp(FILE_VMP)

        # Load NII
        if iterContrast == 'BOLD':
            NII = nib.load(os.path.join(PATH_NII, "BOLD_interp.nii"))
        else:
            NII = nib.load(os.path.join(PATH_NII, "VASO_interp_LN.nii"))

        # Find new VMP dims
        dim_nii = np.asarray(NII.shape)
        dim_vmp = np.asarray(data_vmp.shape)
        offset = np.subtract(dim_nii, dim_vmp)
        print(offset)

        # Update VMP header
        new_vmp_header = copy(header_vmp)

        if offset[0] > 1:
            new_vmp_header['ZStart'] = new_vmp_header['ZStart'] - (offset[0]-1)
            new_vmp_header['ZEnd'] = new_vmp_header['ZEnd'] + (offset[0]-1)
        else:
            #new_vmp_header['ZEnd'] = new_vmp_header['ZEnd'] + offset[0]
            new_vmp_header['ZStart'] = new_vmp_header['ZStart'] - offset[0]

        if offset[1] > 1:
            new_vmp_header['XStart'] = new_vmp_header['XStart'] - (offset[1]-1)
            new_vmp_header['XEnd'] = new_vmp_header['XEnd'] + (offset[1]-1)
        else:
            #new_vmp_header['XEnd'] = new_vmp_header['XEnd'] + offset[1]
            new_vmp_header['XStart'] = new_vmp_header['XStart'] - offset[1]

        if offset[2] > 1:
            new_vmp_header['YStart'] = new_vmp_header['YStart'] - (offset[2]-1)
            new_vmp_header['YEnd'] = new_vmp_header['YEnd'] + (offset[2]-1)
        else:
            #new_vmp_header['YEnd'] = new_vmp_header['YEnd'] + offset[2]
            new_vmp_header['YStart'] = new_vmp_header['YStart'] - offset[2]

        # To print the corrected dims match
        # ===================================================
        z = new_vmp_header['ZEnd'] - new_vmp_header['ZStart']
        x = new_vmp_header['XEnd'] - new_vmp_header['XStart']
        y = new_vmp_header['YEnd'] - new_vmp_header['YStart']

        # print("New vmp dimesions: {}".format(dim_templ))
        print("Assigned vmp dimensions: [{} {} {}]".format(z, x, y))
        # # # ===================================================

        # Update VMP data
        new_data_vmp = np.zeros([256, 256, 256, 5])
        new_data_vmp[header_vmp['ZStart']:header_vmp['ZEnd'],
                      header_vmp['XStart']:header_vmp['XEnd'],
                      header_vmp['YStart']:header_vmp['YEnd']] = data_vmp

        # Extract the big version
        final_vmp = new_data_vmp[new_vmp_header['ZStart']:new_vmp_header['ZEnd'],
                      new_vmp_header['XStart']:new_vmp_header['XEnd'],
                      new_vmp_header['YStart']:new_vmp_header['YEnd']]

        # Save updated VMP
        basename = FILE_VMP.split(os.extsep, 1)[0]

        OUTNAME = "{}_fix_dim.vmp".format(basename)
        bvbabel.vmp.write_vmp(OUTNAME, header_vmp, data_vmp)

print("Done.")
