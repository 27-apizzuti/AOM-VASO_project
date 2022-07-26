"""
Created on 21/01/22

    Winner Maps, Preference Maps, new Sensitivity and Specificity

    1. Read nifti t-maps (from: _meanRuns_noNORDIC_ROI_sub-02_leftMT_Sphere16radius_c_thr0.vmp) and nifti ROI
    2. Voxels selection into ROI
    3. Compute Winner Maps (max operator)-map1
    4. Compute Sensitivity (t-values euclidian norm)-map2
    5. Compute Specificity [1-div=1-arcsen( dot(x,y)/norm(x)norm(y) )] /60 (max angle possible)-map3
    6. Save new nifti


INPUT: nifti
OUTPUT: nifti

NOTE:
    Maps oder in .vmp: 1) Horizontal, 2) Vertical 3) Diag45 4) Diag135
    Multiple subjects possible
    Multiple ROI

@author: apizz

"""

import os
import numpy as np
import nibabel as nb

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
ROI_NAME = ["leftMT_Sphere16radius"]

for su in SUBJ:

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'maps')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    for roi in ROI_NAME:
        for fu in FUNC:
            print("Processing {} {} ROI {}".format(fu, su, roi))

            TMAPS_NII = "{}_{}_{}_tmaps.nii.gz".format(su, fu, roi)
            ROI_NII = "{}_{}.nii.gz".format(su, roi)

            # Read nifti tmaps
            nii1 = nb.load(os.path.join(PATH_IN, TMAPS_NII))
            nii_tmaps = nii1.get_fdata()

            # Read nifti ROI
            nii2 = nb.load(os.path.join(PATH_IN, ROI_NII))
            vox_roi = nii2.get_fdata()

            # Find indices inside ROI (binary mask)
            vox_idx = vox_roi > 0

            # Get t-values inside ROI
            vox_tvalue = nii_tmaps[vox_idx, 0:4]

            # Check negative t-values and put to zero
            vox_neg = vox_tvalue < 0
            vox_tvalue[vox_neg] = 0

            # Compute Winner/Preference Map
            vox_label = np.zeros(len(vox_tvalue))
            for it in range(0, len(vox_tvalue)):
                if np.sum(vox_tvalue[it] > 0):
                    vox_label[it] = np.argmax(vox_tvalue[it, :], axis=-1) + 1

            # Compute Metric #1: Norm (Euclidian Distance)-Sensitivity
            vox_norm = np.linalg.norm(vox_tvalue, ord=None, axis=1, keepdims=False)

            # Compute Metric #2: Divergence-Specificity
            # NOTE: [0-60° max] --> normalized into [0-1]
            t_asc = np.sort(vox_tvalue, axis=1)
            v = [0, 0, 0, 1]              # reference axis (winning)
            vox_div = np.zeros([t_asc.shape[0]])

            for iterVox in range(0, t_asc.shape[0]):
                u = t_asc[iterVox, :]
                if np.sum(u) > 0:
                    c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) # -> cosine of the angle
                    angle = np.arccos(np.clip(c, -1, 1))                # -> radiants
                    angle_degree = angle * 180 / np.pi                  # -> degree
                    if angle_degree < 0:
                        print("Vectors: {}, {}".format(u, v))
                    vox_div[iterVox] = angle_degree / 60                # -> normalization
                    vox_div[iterVox] = 1 - vox_div[iterVox]             # -> inverted
                    if vox_div[iterVox] > 1:
                        print("Vectors: {}, {}; spec. {}, angle: {}".format(u, v, vox_div[iterVox], angle_degree))
            print(np.max(vox_div))
            # %% Save nifti
            # Export UNTHRESHOLDED WINNER MAP
            new_data = np.zeros(np.shape(vox_idx))
            new_data[vox_idx] = vox_label
            outname = os.path.join(PATH_OUT, "{}_{}_{}_winner_map.nii.gz".format(su, roi, fu))
            img = nb.Nifti1Image(new_data, affine=nii1.affine)
            nb.save(img, outname)

            # Export UNTHRESHOLDED SENSITIVITY MAP
            new_data = np.zeros(np.shape(vox_idx))
            new_data[vox_idx] = vox_norm
            outname = os.path.join(PATH_OUT, "{}_{}_{}_sensitivity_map.nii.gz".format(su, roi, fu))
            img = nb.Nifti1Image(new_data, affine=nii1.affine)
            nb.save(img, outname)

            # Export UNTHRESHOLDED SPECIFICITY MAP
            new_data = np.zeros(np.shape(vox_idx))
            new_data[vox_idx] = vox_div
            outname = os.path.join(PATH_OUT, "{}_{}_{}_specificity_map.nii.gz".format(su, roi, fu))
            img = nb.Nifti1Image(new_data, affine=nii1.affine)
            nb.save(img, outname)


print("Done.")
