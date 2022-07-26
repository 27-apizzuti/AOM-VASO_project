"""
Created on Sat Jan 22 11:17:34 2022

    Scatterplot (sub-plot): Voxel-wise Specificity vs Sensitivity (single-subject)

INPUT: nifti Sensitivity and nifti Specificity
OUTPUT: figures

NOTES: Run separately for ROI (left, right) reference impliced in VMP filename

@author: apizz
"""
import os
import matplotlib.pyplot as plt
import nibabel as nb
import numpy as np


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
ROI_NAME = 'leftMT_Sphere16radius'
# MASK = ["BOLD_FDR_mask", "BOLD_FDR_mask"]
MASK = ["CV_BOLD_mask", "CV_VASO_mask"]
# MASK = "" # if you don't have mask

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'ScatterPlot')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)


red_dots = None  # Just to initialize
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)

for i, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'masks')
    for j, fu in enumerate(FUNC):
        SENS_NII = "{}_{}_{}_sensitivity_map.nii.gz".format(su, ROI_NAME, fu)
        SPEC_NII = "{}_{}_{}_specificity_map.nii.gz".format(su, ROI_NAME, fu)
        ROI_NII = "{}_{}.nii.gz".format(su, ROI_NAME)

        # Read nifti sensitivity
        nii1 = nb.load(os.path.join(PATH_IN, 'maps', SENS_NII))
        nii_sens = nii1.get_fdata()

        # Read winner map
        nii2 = nb.load(os.path.join(PATH_IN, 'maps', SPEC_NII))
        nii_spec = nii2.get_fdata()

        # Read nifti ROI
        nii2 = nb.load(os.path.join(PATH_IN, ROI_NII))
        vox_roi = nii2.get_fdata()
        idx1 = vox_roi > 0

        if len(MASK) > 0 :

            MASK_NII = "{}_{}_{}.nii.gz".format(su, ROI_NAME, MASK[j])
            nii4 = nb.load(os.path.join(PATH_MASK, MASK_NII))
            mask = nii4.get_fdata()
            mask_name = "{}_{}".format(MASK[0], MASK[1])
            idx2 = mask > 0
            idx = idx2 * idx1
        else:
            idx = idx1
            mask_name = "no_mask"

        # Plotting
        vox_sens = nii_sens[idx]
        vox_spec = nii_spec[idx]
        axs[j, i].scatter(vox_sens,
                          vox_spec,
                          color='black',
                          alpha=0.2)
        axs[j, i].set_ylabel("Specificity (1-div)")
        axs[j, i].set_xlabel("Sensitivity (L2norm)")
        axs[j, i].set_ylim([0, 1])
        axs[j, i].set_xlim([0, 30])
        axs[j, i].grid("True")
        axs[j, i].set_title("{} {}".format(su, fu))

plt.suptitle("Voxel Characterization {} ({})\n\n".format(ROI_NAME, mask_name))
fig_filename = "All_sbj_{}_Voxel_Characterization_{}".format(
    ROI_NAME, CONDT[0], mask_name)
fig.tight_layout()
plt.savefig(os.path.join(PATH_OUT, fig_filename),
            bbox_inches='tight', dpi=my_dpi)
plt.show()
