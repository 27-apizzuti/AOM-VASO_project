"""
Created on Sat Jan 22 11:50:26 2022
Group Result
Create Tuning Curves Averaged across subjects (AVG or CV);
Load all the subjects at once and make a unique plot
Info stored: -Tuning Sensitivity; -#vox per motion direction

@author: apizz

"""
import os
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nb
import scipy.stats

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD", "VASO"]
ROI_NAME = "leftMT_Sphere16radius"
MASK = ["CV_BOLD_mask", "CV_VASO_mask"]
# MASK = ""

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'WinnerMaps')

if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Output variables
t_values_allSbj = [[], [], [], []], [[], [], [], []]
n_vox_allSbj = np.zeros([2, len(SUBJ), 4, 2])

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                            'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8')
    PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                            'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt8', 'masks')

    for iterfu, fu in enumerate(FUNC):

        TMAPS_NII = "{}_{}_{}_tmaps.nii.gz".format(su, fu, ROI_NAME)
        WINNER_NII = "{}_{}_{}_winner_map.nii.gz".format(su, ROI_NAME, fu)
        ROI_NII = "{}_{}.nii.gz".format(su, ROI_NAME)

        # Read nifti tmaps
        nii1 = nb.load(os.path.join(PATH_IN, TMAPS_NII))
        nii_tmaps = nii1.get_fdata()
        nii_tmaps = nii_tmaps[..., 0:4]

        # Read nifti ROI
        nii2 = nb.load(os.path.join(PATH_IN, ROI_NII))
        vox_roi = nii2.get_fdata()
        idx1 = vox_roi > 0

        # Read winner map
        nii3 = nb.load(os.path.join(PATH_IN, 'maps', WINNER_NII))
        nii_win = nii3.get_fdata()

        if len(MASK) > 0 :

            MASK_NII = "{}_{}_{}.nii.gz".format(su, ROI_NAME, MASK[iterfu])
            nii4 = nb.load(os.path.join(PATH_MASK, MASK_NII))
            mask = nii4.get_fdata()
            mask_name = "{}_{}".format(MASK[0], MASK[1])
            idx2 = mask > 0
            idx = idx2 * idx1
        else:
            idx = idx1
            mask_name = "no_mask"

        # Extract voxel tvalue for each class and compute tuning
        vox_tvalue = nii_tmaps[idx, :]
        vox_label = nii_win[idx]

        for k, j in enumerate(range(1, 5)):
            vox_data = vox_tvalue[vox_label == j, :]
            t_values_allSbj[iterfu][k].append(vox_data)
            n_vox_allSbj[iterfu, iterSbj, k, 0] = vox_data.shape[0]
            n_vox_allSbj[iterfu, iterSbj, k, 1] = vox_data.shape[0] / vox_tvalue.shape[0] * 100

# Avregaging across subjects
tuning_sel = np.zeros([2, 4])
tuning = np.zeros([2, 4, 4, 2])   # contrast, class, class, mean, std
for i in range(0, 2):
    n = np.sum(np.sum(n_vox_allSbj[i,:, 0], axis=1))

    for j in range(0, 4):
        x = np.vstack(t_values_allSbj[i][j])
        m = np.mean(x, axis=0)
        tuning[i, j, :, 0] = m
        tuning[i, j, :, 1] = scipy.stats.sem(x, axis=0)
        # Compute tuning selectivity
        mask = np.ones(4)
        mask[j] = 0
        tuning_sel[i, j] = m[j] / np.mean(m[mask > 0])

# Compute averaged percentage across subjects
bold_tot = np.sum(np.sum(n_vox_allSbj[0, :, :, 0]))
bold_cat = np.sum(n_vox_allSbj[0, :, :, 0], axis=0)
bold_cat_perc = (bold_cat/bold_tot) *100

vaso_tot = np.sum(np.sum(n_vox_allSbj[1, :, :, 0]))
vaso_cat = np.sum(n_vox_allSbj[1, :, :, 0], axis=0)
vaso_cat_perc = (vaso_cat/vaso_tot) *100


# %% Plotting: Tuning curves
my_dpi = 96
x = np.array([1, 2, 3, 4])
fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(1920/my_dpi, (1080/2)/my_dpi), dpi=my_dpi)
contrast = ["Horizontal", "Vertical", "Diagonal 45°-225°", "Diagonal 135°-315°"]

for k in range(0, 4):
    axs[k].errorbar(x, tuning[0, k, :, 0], tuning[0, k, :, 1], color='black', label='BOLD')
    axs[k].errorbar(x, tuning[1, k, :, 0], tuning[1, k, :, 1], color='red', label='VASO')

    axs[k].axvspan(x[k]-0.5, x[k]+0.5, facecolor='#2ca02c', alpha=0.5)
    axs[k].set_title("{}, [B {:.2f}, V {:.2f}]".format(contrast[k], tuning_sel[0, k], tuning_sel[1, k]))
    axs[k].set_xticks(x)
    axs[k].set_ylim([0, 5.5])
    axs[k].set_ylabel("T-value")
    axs[k].set_xlabel("Conditions")
    axs[k].legend();

plt.suptitle('Group results: Tuning curves ({}) {}'.format(mask_name, ROI_NAME))
fig_filename = "Group_results_{}_Tuning_Curves_{}_{}range_0_5_noshadow".format(mask_name, ROI_NAME, CONDT[0])
plt.savefig(os.path.join(PATH_OUT, "tiny_{}.svg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.savefig(os.path.join(PATH_OUT, "Tiny_{}.png".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.show()

# %% Plotting: Voxels per motion direction (barplot) (all subject)
my_dpi = 96
contrast = ["Horizontal", "Vertical", "Diagonal 45°-225°", "Diagonal 135°-315°"]

n_sbj = 5  # number of subjects
ind = np.arange(n_sbj)
width = 0.2

n_con = 4  # number of conditions
cond_colors = ['tab:red', 'tab:cyan', 'tab:green', 'tab:pink']
for j, f in enumerate(FUNC):
    for i in range(0, n_con):
        cond = n_vox_allSbj[j, :, i, 1]  # all subject, single condition (5 elements)
        bar = plt.bar(ind+width*i, cond, width, color = cond_colors[i])

    plt.xlabel("Axis of Motion")
    plt.ylabel("Percentage of Voxels (%)")
    plt.title("{}".format(f))
    plt.ylim(0, 50)

    plt.xticks(ind+width)
    plt.legend(contrast)

    fig_filename = "AllSbj_{}_{}_BarPlot_{}_{}".format(mask_name, f, ROI_NAME, CONDT[0])
    plt.savefig(os.path.join(PATH_OUT, "{}.svg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
    plt.savefig(os.path.join(PATH_OUT, "{}.jpeg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
    plt.show()

# %% Plotting: Voxels per motion direction (barplot) (group average)

my_dpi = 96
contrast = ["Horizontal", "Vertical", "Diagonal 45°-225°", "Diagonal 135°-315°"]

n_const = 2
ind = np.arange(n_const)
width = 0.2
n_con = 4  # number of conditions
for i in range(0, n_con):
    b = np.array([bold_cat_perc[i], vaso_cat_perc[i]])  # Bold and Vaso, single condition (2 elements)
    bar = plt.bar(ind+width*i, b, width, color=cond_colors[i])

plt.xlabel("Constrasts")
plt.ylabel("Percentage of Voxels (%)")
plt.ylim(0, 40)

plt.xticks(ind+width)
plt.legend(contrast)

fig_filename = "Group_results_{}_BarPlot_{}_{}".format(mask_name, ROI_NAME, CONDT[0])
plt.savefig(os.path.join(PATH_OUT, "{}.svg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.savefig(os.path.join(PATH_OUT, "{}.jpeg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.show()

# %% Plotting: Tuning selectivity BOLD and VASO (barplot) (group average)
my_dpi = 96
contrast = ["Horizontal", "Vertical", "Diagonal 45°-225°", "Diagonal 135°-315°"]

n_const = 2
ind = np.arange(n_const)
width = 0.2
n_con = 4  # number of conditions

for i in range(0, n_con):
    b = np.array([tuning_sel[0, i], tuning_sel[1, i]])  # Bold and Vaso, single condition (2 elements)
    bar = plt.bar(ind+width*i, b, width, color=cond_colors[i])

plt.xlabel("Constrasts")
plt.ylabel("Tuning Selectivity")

plt.xticks(ind+width)
plt.legend(contrast)

fig_filename = "Group_results_{}_TuningSelectivity_{}_{}".format(mask_name, ROI_NAME, CONDT[0])
plt.savefig(os.path.join(PATH_OUT, "{}.svg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.savefig(os.path.join(PATH_OUT, "{}.jpeg".format(fig_filename)), bbox_inches='tight', dpi=my_dpi)
plt.show()
