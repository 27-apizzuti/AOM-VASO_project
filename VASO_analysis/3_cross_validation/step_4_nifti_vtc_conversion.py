""" Read nifti and export vtc

It loads CV BOCO's output: BOLD_interp.nii and VASO_interp_LN.nii
and .VTC template from the main analysis path
(BOCO -> Matlab Neuroelf .FMR -> import in BV and create identical VMR/VTC ->
fix dims of VTC with BVBABEL put back nifti BOCO data)

Once NII is imported:
    .nii x, y, z, k --> .vtc 1) -x, y, z    (on the nii.data)
                             2) update header (dims = z, x, y)

    If VASO data =* 30000

Updated on Wed Sep 29 2021

@author: apizz
"""

import os
import bvbabel
import nibabel as nib
import numpy as np
from copy import copy
from glob import glob

print("Hello!")

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONTR = ["BOLD_interp", "VASO_interp_LN"]
PROC = "standard"

# =============================================================================
for iterSbj in SUBJ:

    # Load nifti
    PATH_IN = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'cross_validation')
    FLD_IN = glob(os.path.join(PATH_IN, "run*", ""))

    for iterFLD in FLD_IN:
        CV_FLD_IN = os.path.join(iterFLD, 'boco')
        OUT_FLD = os.path.join(iterFLD, 'GLM')

        if not os.path.exists(OUT_FLD):
            os.mkdir(OUT_FLD)

        for iterContrast in CONTR:
            print('Working on {} {} contrast {}'.format(iterSbj, iterFLD, iterContrast))
            FILE_NII = os.path.join(CV_FLD_IN, '{}.nii').format(iterContrast)
            NII = nib.load(FILE_NII)

            # Load template VTC
            PATH_VTC = os.path.join(STUDY_PATH, iterSbj, 'derivatives', 'func', 'AOM', 'vaso_analysis', PROC, 'GLM')
            FILE_VTC = os.path.join(PATH_VTC, '{}_NeuroElf_IDENTITY_fixdim.vtc').format(iterContrast)
            header_vtc, data_vtc = bvbabel.vtc.read_vtc(FILE_VTC)

            dim_nii = np.asarray(NII.shape)
            dim_vtc = np.asarray(data_vtc.shape)

            offset = np.subtract(dim_nii, dim_vtc)
            print(offset, "referred to data")

            # Update data VTC
            new_data_vtc = NII.get_fdata()
            new_data_vtc = new_data_vtc[::-1, :, :, :]

            if iterContrast == "VASO_interp_LN":
                new_data_vtc = new_data_vtc*30000

            # Update VTC header
            new_vtc_header = copy(header_vtc)

            # To print the corrected dims match
            # ===================================================
            z = new_vtc_header['ZEnd'] - new_vtc_header['ZStart']
            x = new_vtc_header['XEnd'] - new_vtc_header['XStart']
            y = new_vtc_header['YEnd'] - new_vtc_header['YStart']
            print("Nifti dimesions : {}".format(dim_nii))
            print("Assigned vtc dimensions: [{} {} {}]".format(z, x, y))
            # ===================================================

            # Save new VTC
            basename = os.path.join(OUT_FLD, '{}'.format(iterContrast))

            OUTNAME = "{}_bvbabel.vtc".format(basename)
            bvbabel.vtc.write_vtc(OUTNAME, new_vtc_header, new_data_vtc)

print("Done.")
