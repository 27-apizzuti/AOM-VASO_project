"""
Created on Thu Jan 20 11:15:22 2022

Depth-dependent Sensitivity, Specificity, EPI intensity

(2D histogram)
@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib as mpl


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI_NAME = 'leftMT_Sphere16radius'
MASKS = 'CV_AVG'

tag_thr = [185]

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'EPI_vessels')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Figure preparation
plt.style.use('dark_background')
my_dpi = 300
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(1920/my_dpi, 1080/my_dpi),
            dpi=my_dpi)
for j, su in enumerate(SUBJ):

    PATH_EPI = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2')

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

    # Import ROI file
    FILE = os.path.join(PATH_EPI, '{}_{}_scaled_4.nii.gz'.format(su, ROI_NAME))
    nii = nb.load(FILE)
    roi = nii.get_fdata()
    idx_roi = roi > 0

    # Import EPI file
    FILE = os.path.join(PATH_EPI, 'BOLD_mean_leftMT_Sphere16radius_scaled_4.nii.gz')
    nii = nb.load(FILE)
    EPI = nii.get_fdata()
    dims = np.shape(EPI)

    # Apply segmentation to EPI file
    # Find tag voxels in gray matter
    idx_tag = EPI < tag_thr[j]
    idx = idx_tag * idx_gm * idx_roi
    EPI_temp = EPI[idx]
    c_EPI = np.sum(idx)  # count EPI
    idx_EPI = idx_gm * idx_roi
    print("For {}, number of tag_vox (gm) EPI: {}, [mean, std]: [{},{}]".format(su, c_EPI, np.mean(EPI_temp), np.std(EPI_temp)))

    #### Save tag_vox as segmentation
    new_data = np.zeros(dims)
    new_data[idx] = 1
    # outname = os.path.join(PATH_OUT, "{}_{}_tagged_voxels.nii.gz".format(su, ROI_NAME))
    # img = nb.Nifti1Image(new_data, affine=nii.affine)
    # nb.save(img, outname)

    for i, fu in enumerate(FUNC):

        # Import mask
        FILE = os.path.join(PATH_EPI, "masks", "{}_{}_{}_{}_mask_scaled_4.nii.gz".format(su, ROI_NAME, fu, MASKS))
        nii = nb.load(FILE)
        mask = nii.get_fdata()
        idx_mask = mask > 0
        n_vox_avg_cv = np.sum(idx_mask)

        # Import sensitivity map
        FILE = os.path.join(PATH_EPI, 'maps', "{}_{}_{}_sensitivity_map_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        sens_map = nii.get_fdata()
        if i ==0:
            idx_sens = sens_map > 10
        else:
            idx_sens = sens_map > 5


        # Import specificity map
        FILE = os.path.join(PATH_EPI, 'maps', "{}_{}_{}_specificity_map_scaled_4.nii.gz".format(su, ROI_NAME, fu))
        nii = nb.load(FILE)
        spec_map = nii.get_fdata()
        # Clip 0-1
        spec_map[spec_map < 0] = 0
        spec_map[spec_map > 1] = 1

        #------- apply mask and count
        # idx = idx_mask * idx_gm * idx_roi
        idx2 = idx_mask * idx_gm * idx_tag * idx_roi
        n_vox_tag = np.sum(idx2)  # count EPI
        perc = (n_vox_tag/n_vox_avg_cv) * 100

        se = np.mean(sens_map[idx2])
        sp = np.mean(spec_map[idx2])
        print("For {} {}, for tag_vox (gm) EPI in {}, [Sens, Spec]: {}, {}]".format(su, fu, MASKS, se, sp))

        # # 2D histogram: only tag voxels
        # n_bins = [50, 50]
        # im = axs[i, 0].hist2d(metric[idx*idx_sens], sens_map[idx*idx_sens], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        # im = axs[i, 1].hist2d(metric[idx*idx_sens], spec_map[idx*idx_sens], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        # # axs[i, 0].set_xlabel("Normalized cortical depth")
        # # axs[i, 1].set_xlabel("Normalized cortical depth")
        # # axs[i, 0].set_ylabel("Sensitivity {}".format(fu))
        # # axs[i, 1].set_ylabel("Specificity {}".format(fu))
        # axs[i, 0].set_ylim((0.02, 25))
        # axs[i, 1].set_ylim((0.02, 1))
        # axs[i, 0].set_xlim((0, 1))
        # axs[i, 1].set_xlim((0, 1))
        # fig_filename = "{}_Sens_Spec_tag_EPI_voxels".format(su)

        # 2D histogram: all ROI voxels
        # n_bins = [50, 50]
        # im = axs[i, 0].hist2d(metric[idx_EPI], sens_map[idx_EPI], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        # im = axs[i, 1].hist2d(metric[idx_EPI], spec_map[idx_EPI], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        # # axs[i, 0].set_xlabel("Normalized cortical depth", fontsize=20)
        # # axs[i, 1].set_xlabel("Normalized cortical depth", fontsize=20)
        # # axs[i, 0].set_ylabel("Sensitivity {}".format(fu), fontsize=20)
        # axs[i, 0].set_ylim((0.02, 25))
        # axs[i, 1].set_ylim((0.02, 1))
        # axs[i, 0].set_xlim((0, 1))
        # axs[i, 1].set_xlim((0, 1))
        # fig_filename = "{}_Sens_Spec_tag_ROI_voxels".format(su)

        # 2D histogram: all ROI voxels
        n_bins = [50, 50]
        im = axs[i, 0].hist2d(metric[idx_EPI], EPI[idx_EPI], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        im = axs[i, 1].hist2d(metric[idx*idx_sens], EPI[idx*idx_sens], bins=n_bins, cmap='magma', norm=mpl.colors.LogNorm())
        # axs[i, 0].set_ylim((0.02, 500))
        # axs[i, 1].set_ylim((0.02, 500))
        axs[i, 0].set_xlim((0, 1))
        axs[i, 1].set_xlim((0, 1))
        fig_filename = "{}_EPI_tag_ROI_voxels".format(su)



# Save figure
fig.tight_layout()
plt.savefig(os.path.join(PATH_OUT, "{}.svg".format(fig_filename)),
        bbox_inches='tight', dpi=my_dpi)
plt.savefig(os.path.join(PATH_OUT, "{}.jpeg".format(fig_filename)),
        bbox_inches='tight', dpi=my_dpi)
plt.show()
