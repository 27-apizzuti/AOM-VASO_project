"""
Created on Wed Mar  2 10:21:53 2022

Columnar volume as function of the columnarity index.

The user has to enter FILES and DOMAIN variable.

# DOMAIN is only one file
# FILES can be multiple if the domain is the same (e.g FDR_BOLD domain)

@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
RADIUS_DISK = [15, 13, 12, 13, 16]
OUTPUT_DIR = 'D:\Pilot_Exp_VASO\pilotAOM\Results\Conv_Columns'

# Columnarity index range
threshold = np.arange(0.20, 1, 0.05)  # columnarity index range

# Prepare plot and output variable
my_dpi = 200
fig, ax = plt.subplots(nrows=1, ncols=1)
domain_volume = np.zeros(np.size(SUBJ))
columns_volume_ratio = np.zeros([np.size(threshold), np.size(SUBJ), 2])
vox_vol = 0.2 * 0.2 * 0.2

for iterSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'columns')
    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS_DISK[iterSbj]))

    FILES = ['{}_{}_BOLD_FDR_BOLD_columns_full_depth_UVD_columns_mode_filter_window_count_ratio'.format(su, ROI),
         '{}_{}_BOLD_FDR_VASO_columns_full_depth_UVD_columns_mode_filter_window_count_ratio'.format(su, ROI)]

    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin_masked_BOLD_FDR_full_depth.nii.gz'.format(su))

    for it_file, file in enumerate(FILES):

        nii1 = nb.load(os.path.join(PATH_IN, '{}.nii.gz'.format(file)))  # Get columnar data
        data = nii1.get_fdata()

        nii2 = nb.load(DOMAIN)  # Get domain data
        domain_data = nii2.get_fdata()
        idx_domain = domain_data > 0
        domain_volume[iterSbj] = np.sum(idx_domain) *vox_vol  # Compute domain volume

        print("For {}, domain_volume = {:1f} mm3".format(su, domain_volume[iterSbj]))
        columns_volume = np.zeros(np.size(threshold))

        for it_thr, thr in enumerate(threshold):
            # Compute columns volume
            idx_thr = data > thr
            columns_volume[it_thr] = np.sum(idx_thr) *vox_vol
            columns_volume_ratio[it_thr, iterSbj, it_file] = (columns_volume[it_thr]/domain_volume[iterSbj])*100

        # Plot columns_volume_ratio as lineplot
        if it_file == 0:
            plt.plot(threshold*100, columns_volume_ratio[:, iterSbj, it_file], 'b')  # BOLD
        else:
            plt.plot(threshold*100, columns_volume_ratio[:, iterSbj, it_file], 'r')  # VASO
        # plt.vlines(0.65, 0, 100, colors='k', linestyles='dashed')
        # ax.set_xticks(threshold[0::2])
        # ax.set_xticklabels(threshold[0::2]*100)
        plt.xlabel("Columnarity index")
        plt.ylabel("% Columnar Volume")
        plt.grid()
        # plt.title("Group result: columnar volume as function of columnar index (C.I.)")

# Save plot
plt.savefig(os.path.join(OUTPUT_DIR,'columnar_volumes_BOLD_FDR_AllSbj.jpeg'), bbox_inches='tight')
plt.savefig(os.path.join(OUTPUT_DIR,'columnar_volumes_BOLD_FDR_AllSbj.svg'), bbox_inches='tight')
plt.show()
# -------------------------------------------
# Horizontal stacked bar plot
my_dpi = 96
fig, ax = plt.subplots(figsize=(1920/my_dpi, 540/my_dpi))
plt.style.use('dark_background')

labels = ['S1', 'S2', 'S3', 'S4', 'S5']
row = 14  # threshold[14] = 0.6666
BOLD_value = columns_volume_ratio[row, :, 0]
VASO_value = columns_volume_ratio[row, :, 1]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
ax.yaxis.grid()
rects1 = ax.bar(x - width/2, BOLD_value, width, label='BOLD')
rects2 = ax.bar(x + width/2, VASO_value, width, label='VASO')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('% columnar volume')
ax.set_title('Group result: columnar volume fraction for BOLD and VASO')
ax.set_xticks(x)
ax.set_xticklabels(labels)

ax.legend()

# fig.tight_layout()
plt.show()
fig.savefig(os.path.join(OUTPUT_DIR,'barplot_columnar_volumes_at_65_BOLD_FDR_AllSbj.jpeg'), bbox_inches='tight')
fig.savefig(os.path.join(OUTPUT_DIR,'barplot_columnar_volumes_at_65_BOLD_FDR_AllSbj.svg'), bbox_inches='tight')
