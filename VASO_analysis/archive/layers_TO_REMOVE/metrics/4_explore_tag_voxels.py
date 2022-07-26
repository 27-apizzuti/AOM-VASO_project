"""
Created on Thu Jan 20 11:15:22 2022

Counting EPI voxels that look like vessels in:
    - segmented gray matter (initial ref)
    - BOLDmask
    - CV BOLD and CV VASO

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
# SUBJ = ['sub-02']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI_NAME = 'leftMT_Sphere16radius'
MASKS = 'CV_AVG'

tag_thr = 150

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'DrainVeins')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Figure preparation
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=5, figsize=(1920/my_dpi, 1080/my_dpi),
            dpi=my_dpi)
for j, su in enumerate(SUBJ):

    PATH_EPI = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2')

    PATH_SEG = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'segmentation_4')

    PATH_LAY = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4')


    # Import metric file
    FILE = os.path.join(PATH_LAY, '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    nii = nb.load(FILE)
    metric = nii.get_fdata()
    idx_gm = metric > 0

    # Import UNI file
    FILE = os.path.join(PATH_SEG, '{}_acq-mp2rage_UNI_ss_warp_resl_slab_scaled_4.nii'.format(su))
    nii = nb.load(FILE)
    UNI_gm = nii.get_fdata()

    # Import EPI file
    FILE = os.path.join(PATH_EPI, 'BOLD_mean_leftMT_Sphere16radius_scaled_4.nii.gz')
    nii = nb.load(FILE)
    EPI = nii.get_fdata()
    dims = np.shape(EPI)

    # Apply segmentation to EPI file
    # Find tag voxels in gray matter
    idx_tag = EPI < tag_thr
    idx = idx_tag * idx_gm
    EPI_temp = EPI[idx]
    c_EPI = np.sum(idx)  # count EPI
    print("For {}, number of tag_vox (gm) EPI: {}, [mean, std]: [{},{}]".format(su, c_EPI, np.mean(EPI_temp), np.std(EPI_temp)))

    #### Save tag_vox as segmentation
    new_data = np.zeros(dims)
    new_data[idx] = 1
    outname = os.path.join(PATH_OUT, "{}_{}_tagged_voxels.nii.gz".format(su, ROI_NAME))
    img = nb.Nifti1Image(new_data, affine=np.eye(4))
    nb.save(img, outname)

    for i, fu in enumerate(FUNC):

        # Import mask
        FILE = os.path.join(PATH_EPI, "{}_{}_{}_{}_mask_scaled_4.nii.gz".format(su, ROI_NAME, fu, MASKS))
        nii = nb.load(FILE)
        mask = nii.get_fdata()
        idx_mask = mask > 0
        n_vox_avg_cv = np.sum(idx_mask)

        # Import sensitivity map
        FILE = os.path.join(PATH_EPI, 'winner_maps', "{}_{}_{}_sensitivity_unthreshold_fix_hd_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        sens_map = nii.get_fdata()

        # Import specificity map
        FILE = os.path.join(PATH_EPI, 'winner_maps', "{}_{}_{}_specificity_unthreshold_fix_hd_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        spec_map = nii.get_fdata()

        #------- apply mask and count
        idx2 = idx_mask * idx_gm * idx_tag
        n_vox_tag = np.sum(idx2)  # count EPI
        perc = (n_vox_tag/n_vox_avg_cv) * 100

        se = np.mean(sens_map[idx2])
        sp = np.mean(spec_map[idx2])
        print("For {} {}, for tag_vox (gm) EPI in {}, [Sens, Spec]: {}, {}]".format(su, fu, MASKS, se, sp))

        # # Scatterplot Sens vs Spec
        # axs[i, j].scatter(sens_map[idx], spec_map[idx], color='black', alpha=0.2)
        # axs[i, j].scatter(sens_map[idx2], spec_map[idx2], color='red', alpha=0.2)
        # axs[i, j].set_xlabel("Sensitivity (L2norm)")
        # axs[i, j].set_ylabel("Specificity (1-div)")
        # axs[i, j].grid("True")
        # axs[i, j].set_title("{}, {}, {}/{} ({}%)\n".format(su, fu, n_vox_tag, n_vox_avg_cv, int(perc)))
        # fig_filename = "AllSbj_Sens_spec_tag_voxel_mask_{}".format(MASKS)

        # # Scatterplot Sens vs depth
        # axs[i, j].scatter(metric[idx], sens_map[idx], color='black', alpha=0.2)
        # axs[i, j].scatter(metric[idx2], sens_map[idx2], color='red', alpha=0.2)
        # axs[i, j].set_xlabel("depths")
        # axs[i, j].set_ylabel("Sensitivity (L2norm)")
        # axs[i, j].grid("True")
        # axs[i, j].set_title("{}, {}, {}/{} ({}%)\n".format(su, fu, n_vox_tag, n_vox_avg_cv, int(perc)))
        # fig_filename = "AllSbj_Sens_depth_tag_voxel_mask_{}".format(MASKS)

        # Scatterplot Sens vs depth
        axs[i, j].scatter(metric[idx], spec_map[idx], color='black', alpha=0.2)
        axs[i, j].scatter(metric[idx2], spec_map[idx2], color='red', alpha=0.2)
        axs[i, j].set_xlabel("depths")
        axs[i, j].set_ylabel("Specificity (1-div)")
        axs[i, j].grid("True")
        axs[i, j].set_title("{}, {}, {}/{} ({}%)\n".format(su, fu, n_vox_tag, n_vox_avg_cv, int(perc)))
        fig_filename = "AllSbj_Spec_depth_tag_voxel_mask_{}".format(MASKS)


# Save figure
# plt.suptitle("Sensitivity and Specificity for tagged voxels")
fig.tight_layout()
plt.savefig(os.path.join(PATH_OUT, fig_filename),
        bbox_inches='tight', dpi=my_dpi)
plt.show()
