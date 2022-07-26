"""
Fix VTC dimensions, going back to the original nifti dims (162,216,26,350)

BV removes a dimension when creating VMR/VTC from FMR.

Updated on Fri Sep 24 12:13:05 2021

@author: apizz
"""
import os
import bvbabel
import nibabel as nib
import numpy as np
from copy import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONTR = ["BOLD_interp", "VASO_interp_LN"]
PROC = "standard"

for su in SUBJ:
    for fu in CONTR:
        print("Working on {} {}".format(su, fu))

        PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", "AOM", "vaso_analysis", PROC)

        FILE_NII = os.path.join(PATH_IN, "boco", "{}.nii".format(fu))
        NII = nib.load(FILE_NII)

        FILE_VTC = os.path.join(PATH_IN, "GLM", "{}_NeuroElf_IDENTITY.vtc".format(fu))

        header_vtc, data_vtc = bvbabel.vtc.read_vtc(FILE_VTC)

        dim_nii = np.asarray(NII.shape)
        dim_vtc = np.asarray(data_vtc.shape)

        offset = np.subtract(dim_nii, dim_vtc)
        print(offset, "referred to data")

        # Update data VTC
        new_data_vtc = NII.get_fdata()
        new_data_vtc = new_data_vtc[::-1, :, :, :]

        if fu == "VASO_interp_LN":
            new_data_vtc = new_data_vtc*30000

        # // Change ZEnd index if 1 step offset
        # Update VTC header
        new_vtc_header = copy(header_vtc)

        if offset[0] > 1:
            new_vtc_header['ZStart'] = new_vtc_header['ZStart'] - (offset[0]-1)
            new_vtc_header['ZEnd'] = new_vtc_header['ZEnd'] + (offset[0]-1)
        else:
            new_vtc_header['ZEnd'] = new_vtc_header['ZEnd'] + offset[0]

        if offset[1] > 1:
            new_vtc_header['XStart'] = new_vtc_header['XStart'] - (offset[1]-1)
            new_vtc_header['XEnd'] = new_vtc_header['XEnd'] + (offset[1]-1)
        else:
            new_vtc_header['XStart'] = new_vtc_header['XStart'] - offset[1]

        if offset[2] > 1:
            new_vtc_header['YStart'] = new_vtc_header['YStart'] - (offset[2]-1)
            new_vtc_header['YEnd'] = new_vtc_header['YEnd'] + (offset[2]-1)
        else:
            new_vtc_header['YStart'] = new_vtc_header['YStart'] - offset[2]

        z = new_vtc_header['ZEnd'] - new_vtc_header['ZStart']
        x = new_vtc_header['XEnd'] - new_vtc_header['XStart']
        y = new_vtc_header['YEnd'] - new_vtc_header['YStart']
        print("Assigned vtc dimensions: [{} {} {}]".format(z, x, y))

        # Save new VTC
        basename = FILE_VTC.split(os.extsep, 1)[0]
        OUTNAME = "{}_fixdim.vtc".format(basename)
        bvbabel.vtc.write_vtc(OUTNAME, new_vtc_header, new_data_vtc)

print("Done.")
