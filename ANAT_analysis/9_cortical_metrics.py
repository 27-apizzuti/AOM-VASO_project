"""
Created on Thu Oct 21 13:56:34 2021

Descriptive statistics for hMT ROI (for perimeter chunck)

Histograms:
-curvature
-thickness

Compute volume (used as reference):
-perimeter chunk

@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

# Define Input
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = ['leftMT_Sphere16radius']
RADIUS = [15, 13, 12, 13, 16]

# Define Output
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'CorticalMetrics')
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
fig.suptitle('Thickness and Curvature for perimeter chunck')

for i, su in enumerate(SUBJ):
    n_bins = 50

    # Loading
    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "anat", "layers_4")
    FILE1 = "{}_seg_rim_4_9_curvature.nii".format(su)
    FILE2 = "{}_seg_rim_4_9_thickness.nii".format(su)
    PATH_IN2 = os.path.join(STUDY_PATH, su, "derivatives", "anat", "flattening_4_r_{}_cp_0".format(RADIUS[i]))
    FILE3 = "{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz".format(su)

    nii1 = nb.load(os.path.join(PATH_IN, FILE1))
    curv = nii1.get_fdata()
    curv = curv.flatten()

    nii2 = nb.load(os.path.join(PATH_IN, FILE2))
    thick = nii2.get_fdata()
    thick = thick.flatten()

    nii3 = nb.load(os.path.join(PATH_IN2, FILE3))
    per = nii3.get_fdata()
    per = per.flatten()
    idx = per > 0  # where my perimeter chunk exists

    # ROI volume
    vox_vol = 0.2 * 0.2 * 0.2                    # mm3
    vol = np.sum(idx) * vox_vol
    print("Working {}, volume perimeter chunk MT: {:.1f} cm3".format(su, vol/1000))

    # ROI mean thickness
    thick_mean = np.mean(thick[idx])
    thick_std = np.std(thick[idx])
    thick_exp = np.sum((thick[idx] > 1.5) * (thick[idx] < 3.5))

    print("Working {}, thickness perimeter chunk MT mean, std: ({:.1f}, +/- {:.1f}) mm".format(su, thick_mean, thick_std))
    print("Working {}, volume of chunk MT with expected thick [1.5, 3.5]: {:.1f} cm3, ({:.1f}%)".format(su, (thick_exp*vox_vol)/1000, (thick_exp*vox_vol/vol)*100))

    # ROI curvature
    curv_roi = curv[idx]
    step = (np.max(curv_roi)-np.min(curv_roi))/3

    sul = np.sum(curv_roi < np.min(curv_roi) + step)
    wall = np.sum((curv_roi > np.min(curv_roi) + step) * (curv_roi < np.max(curv_roi) - step))
    gyr = np.sum((curv_roi > np.max(curv_roi) - step) * (curv_roi < np.max(curv_roi)))

    # Thickness
    axs[0, i].hist(thick[idx], bins=n_bins)
    axs[0, i].axvline(thick_mean, color='k', linestyle='solid', linewidth=1)
    axs[0, i].axvline(1.5, color='k', linestyle='dashed', linewidth=1)
    axs[0, i].axvline(3.5, color='k', linestyle='dashed', linewidth=1)
    axs[0, i].set_xlabel("Cortical Thickness (mm)")
    axs[0, i].set_xlim([0, 5])
    axs[0, i].set_ylabel("N. of Grey Matter Voxels")
    axs[0, i].set_title("{} thick: ({:.1f}+/-{:.1f}) cm".format(su, thick_mean, thick_std))

    # Curvature
    axs[1, i].hist(curv[idx], bins=n_bins)
    axs[1, i].set_xlabel("Cortical Curvature (a.u.)")
    axs[1, i].set_ylabel("N. of Grey Matter Voxels")
    axs[1, i].axvline(np.min(curv_roi) + step, color='k', linestyle='dashed', linewidth=1)
    axs[1, i].axvline(np.max(curv_roi) - step, color='k', linestyle='dashed', linewidth=1)
    axs[1, i].set_title("{} [s:{:.1f}%, w:{:.1f}%, g:{:.1f}%]".format(su, (sul*vox_vol/vol)*100, (wall*vox_vol/vol)*100, (gyr*vox_vol/vol)*100))

plt.savefig(os.path.join(PATH_OUT,'per_chunk_{}_cortical_metrics_AllSbj.jpeg'.format(ROI[0])), bbox_inches='tight')
plt.savefig(os.path.join(PATH_OUT,'per_chunk_{}_cortical_metrics_AllSbj.svg'.format(ROI[0])), bbox_inches='tight')
plt.show()
