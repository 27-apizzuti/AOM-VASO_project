"""Read Brainvoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05','sub-06']
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]

# =============================================================================
for su in SUBJ:
    # Reference nifti for affine matrix
    FILE2 = "/mnt/d/Pilot_Exp_VASO/pilotAOM/" + su + "/derivatives/func/AOM/vaso_analysis/brainmask/mean_run1_VASO.nii.gz"
    for co in CONDT:
        for fu in FUNC:
            FILE = "/mnt/d/Pilot_Exp_VASO/pilotAOM/" + su + "/derivatives/func/AOM/vaso_analysis/" + co + "/GLM/" + fu + "_meanRuns_noNORDIC.vmp"
            # Load vmr
            header, data = bvbabel.vmp.read_vmp(FILE)

            # See header information
            pprint.pprint(header)

            # Read another nifti to get the affine matrix
            target_nii = nb.load(FILE2)
            target_nii_size = np.asarray(target_nii.shape)

            # Flip x axis
            data = data[::-1, :, :, 4]

            # Zero pad data
            pad = target_nii_size - np.asarray(data.shape)
            print(pad)
            # Create new pad matrix
            data2 = np.zeros(target_nii_size)

            xpad = target_nii_size[0] - pad[0]
            ypad = target_nii_size[1] - pad[1]
            zpad = target_nii_size[2] - pad[2]
            print(xpad)
            if fu == "VASO":
                data2[0:xpad, 0:ypad, 0:zpad] = -data
            else:
                data2[0:xpad, 0:ypad, 0:zpad] = data

            # Export nifti
            basename = FILE.split(os.extsep, 1)[0]
            outname = "{}_bvbabel.nii.gz".format(basename)
            img = nb.Nifti1Image(data2, affine=target_nii.affine, header=target_nii.header)
            nb.save(img, outname)

            print("Finished.")
