"""
Created on Thu Oct 21 18:45:31 2021

@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04']
CONDT = ['standard']
ROI = ['leftMT_Sphere16radius']
# MASK = ["BOLD_FDR", "BOLD_CV_AVG", "VASO_CV_AVG"]
MASK = ["BOLD_vox", "VASO_vox", "COMM_vox"]


# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=len(MASK), ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
fig.suptitle('Thickness for different masks')

fig2, axs2 = plt.subplots(nrows=len(MASK), ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'LayerProfiles')
n_bins = 10
for i, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "anat", "layers_4")
    FILE1 = "{}_seg_rim_4_9_thickness.nii".format(su)

    nii1 = nb.load(os.path.join(PATH_IN, FILE1))
    thick = nii1.get_fdata()
    thick = thick.flatten()
    idx = thick > 0                          # where my segmentation exists
    thick_mean = np.mean(thick[idx])

    # Import metric files
    FILE2 = "{}_seg_rim_4_9_metric_equivol.nii".format(su)
    nii2 = nb.load(os.path.join(PATH_IN, FILE2))
    metr = nii2.get_fdata()
    metr = metr.flatten()

    for j, mask in enumerate(MASK):

        # Loading voxels
        PATH_MASK = os.path.join(STUDY_PATH, su, "derivatives", "func", "AOM", "vaso_analysis", CONDT[0], "layers_columns", "res_pt2")
        nii2 = nb.load(os.path.join(PATH_MASK, "{}_{}_{}_mask_scaled_4.nii.gz".format(su, ROI[0], mask)))

        mask_data = nii2.get_fdata()
        mask_data = mask_data.flatten()

        # FIG.1) CORTICAL THICKNESS
        y = thick[(mask_data) > 0]

        axs[j, i].hist(y[y > 0], bins=n_bins)
        axs[j, i].axvline(thick_mean, color='k', linestyle='solid', linewidth=1)
        axs[j, i].axvline(1.5, color='k', linestyle='dashed', linewidth=1)
        axs[j, i].axvline(3.5, color='k', linestyle='dashed', linewidth=1)
        axs[j, i].set_xlabel("Cortical Thickness (mm)")
        axs[j, i].set_ylabel("N. of Grey Matter Voxels")
        axs[j, i].set_title("{}, {}".format(su, mask))

        # FIG.2) CORTICAL METRICS
        z = metr[(mask_data) > 0]

        axs2[j, i].hist(z[z > 0], bins=n_bins)
        # axs[j, i].axvline(thick_mean, color='k', linestyle='solid', linewidth=1)
        # axs[j, i].axvline(1.5, color='k', linestyle='dashed', linewidth=1)
        # axs[j, i].axvline(3.5, color='k', linestyle='dashed', linewidth=1)
        axs2[j, i].set_xlabel("Normalized Cortical Depth (mm)")
        axs2[j, i].set_ylabel("N. of Grey Matter Voxels")
        axs2[j, i].set_title("{}, {}".format(su, mask))

fig.tight_layout()
fig.savefig(os.path.join(PATH_OUT,'Thickness_{}_mask_{}'.format(ROI[0], MASK)), bbox_inches='tight')
fig.show()

fig2.tight_layout()
fig2.savefig(os.path.join(PATH_OUT,'Metrics_{}_mask_{}'.format(ROI[0], MASK)), bbox_inches='tight')
fig2.show()
