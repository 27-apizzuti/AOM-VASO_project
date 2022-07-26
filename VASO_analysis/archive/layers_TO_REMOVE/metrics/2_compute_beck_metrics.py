"""
Created on Tue Jan 18 13:42:54 2022

Compute Sensitivity (Beckett2020)

Input: 3D matrix (act. map), 3D matrix (cortical depths)
Output: 3D matrix (beck_sens), 3D matrix (beck_spec)


@author: apizz
"""
import os
import numpy as np
import nibabel as nb
from my_layer_profiles import *
import matplotlib.pyplot as plt

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI_NAME = 'leftMT_Sphere16radius'
MAPS_NAME = ['Vertical', 'Horizontal', 'Diag45', 'Diag135']
n_lay = 21
MASKS = 'CV_AVG'


PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Beckett_estimation')
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Figure preparation
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=5, figsize=(1920/my_dpi, 1080/my_dpi),
        dpi=my_dpi)

for i, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'drain_vein')

    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'layers_columns', 'res_pt2')

    PATH_LAY = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4')

    # Import metric file
    FILE = os.path.join(PATH_LAY, '{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    nii = nb.load(FILE)
    metric = nii.get_fdata()

    # Obtain 21 equidist layers
    metric = metric.flatten()
    idx = metric > 0
    layers = my_layer_profiles(metric[idx], n_lay)
    idx_layers = np.asarray(range(1, n_lay + 1))

    for j, fu in enumerate(FUNC):

        sens_cond = np.zeros([5, 4])
        spec_cond = np.zeros([5, 4])

        print("Working on {}, {}".format(su, fu))

        # FILE2: CV-Mask
        FILE2 = os.path.join(PATH_MASK, "{}_{}_{}_{}_mask_scaled_4.nii.gz".format(su, ROI_NAME, fu, MASKS))
        nii2 = nb.load(FILE2)
        vox_mask = nii2.get_fdata()
        vox_mask = vox_mask.flatten()
        idx_mask = vox_mask[idx] > 0

        # Import activation map (5D)
        FILE = os.path.join(PATH_IN, "{}_{}_{}_5psc_scled_4_unthreshold.nii.gz".format(su, fu, ROI_NAME))
        nii = nb.load(FILE)
        vox_map = nii.get_fdata()

        # Initialize layer-profiles output (4 conditions)
        lay_act = np.zeros([n_lay, 4])

        for it_map, a_map in enumerate(MAPS_NAME):

            # ACTIVATION MAP PER CONDITION (>0)
            vox_map_flat = vox_map[..., it_map].flatten()
            vox_map_flat = vox_map_flat[idx]

            for k, lay in enumerate(idx_layers):
                y = vox_map_flat[(layers == lay) * idx_mask] * 100

                # Layer Profiles (sensitivity measure)
                lay_act[k, it_map] = np.mean(y)
                print(lay_act[k, it_map])

            # Linear regression per condition
            y = lay_act[:, it_map]
            nan_mask = ~np.isnan(y)
            sens = np.mean(y[nan_mask])
            x = np.arange(0, len(y[nan_mask]), 1)
            A = np.vstack([x, np.ones(len(x))]).T
            m, c = np.linalg.lstsq(A, y[nan_mask], rcond=None)[0]
            print("For {}, {}, regression:[m, c] = [{}, {}] ".format(su, fu, m, c))
            print("For {}, {}, sens = {}; inv. spec = {} ".format(su, fu, sens, m))
            sens_cond[i, it_map] = sens
            spec_cond[i, it_map] = m

            # Plot layer profiles per condition
            text_leg = "{}[{:.1f}; {:.3f}]".format(a_map, sens, m)
            axs[j, i].plot(idx_layers, lay_act[:, it_map], linewidth=1, linestyle='-', marker='o', label='{}'.format(text_leg))
            axs[j, i].set_ylim((-1, 11))
            axs[j, i].set_xlabel("Layers (0=white matter)")
            axs[j, i].set_ylabel("Percent Signal Change")
            axs[j, i].grid(True)
            axs[j, i].legend()
            # Plot fitted line
            axs[j, i].plot(idx_layers, (m*idx_layers + c), linewidth=1, linestyle='--')
        # Average across condition
        axs[j, i].set_title("{} {} [{:.1f}, {:.3f}](mean)".format(su, fu, np.mean(sens_cond[i, it_map]), np.mean(spec_cond[i, it_map])))

# Save figure
fig_filename = "AllSbj_cv_layer_profiles_all_contrast_Beckett_metrics"
plt.suptitle("Sensitivity and Inverse Specificity (Beckett2020)")
fig.tight_layout()
plt.savefig(os.path.join(PATH_OUT, fig_filename),
        bbox_inches='tight', dpi=my_dpi)
plt.show()
