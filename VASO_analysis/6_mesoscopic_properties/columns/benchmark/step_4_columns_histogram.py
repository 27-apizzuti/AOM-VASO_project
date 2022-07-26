"""
Created on Tue Feb 22 10:29:54 2022

Evaluate columnar property (empirical data)

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import scipy.stats as stats
import matplotlib.pyplot as plt


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI = 'leftMT_Sphere16radius'
FUNC = ['BOLD', 'VASO']
MASK = 'BOLD_FDR'
# ----------------------------------
PATH_RAND= "C:\\Users\\apizz\\Desktop\\temp_LN2_UVD_FILTER"
RAND_DATA = os.path.join(PATH_RAND, "benchmark_random",
                         "sub-02_hexbin_res_0_UVD_columns_mode_filter_window_count_ratio.8_random_res_0.2_fix_hs.nii.gz")
REG_DATA = os.path.join(PATH_RAND, "benchmark_hexagon_regular",
                         "sub-02_UV_coordinates_hexbins0_UVD_columns_mode_filter_window_count_ratio.5_aom_modulus.nii.gz")
# ---------------------------------

PATH_OUT = "D:\Pilot_Exp_VASO\pilotAOM\Results\Conv_Columns"
if not os.path.exists(PATH_OUT):
    os.mkdir(PATH_OUT)

# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=2, ncols=len(SUBJ)+1, figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
n_bins = 50

for itSubj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, "derivatives", "func", "AOM", "vaso_analysis", "standard", "columns")

    # Loading benchmark dataset
    niir = nb.load(RAND_DATA)
    datar = niir.get_fdata()
    idx_r = (datar > 0) * (datar < 1)
    temp_datar = datar[idx_r]
    density_ran = stats.gaussian_kde(temp_datar)

    niig = nb.load(REG_DATA)
    datag = niig.get_fdata()
    idx_g = (datag > 0) * (datag < 1)
    temp_datag = datag[idx_g]
    density_reg = stats.gaussian_kde(temp_datag)
    # -----------------------------------------

    for itFu, fu in enumerate(FUNC):
        FILE = "{}_{}_{}_{}_columns_full_depth_UVD_columns_mode_filter_window_count_ratio.nii.gz".format(su, ROI, MASK, fu)

        nii = nb.load(os.path.join(PATH_IN, FILE))
        data = nii.get_fdata()
        idx = (data > 0.25) * (data < 1)
        temp_data = data[idx]

        # Plotting
        m = np.mean(temp_data)
        s = np.std(temp_data)
        print("For {}, {} mean {:.1f} +/- {:.1f}".format(su, fu, m, s))
        n, x, _ = axs[itFu, itSubj].hist(temp_data, bins=n_bins, density=True)
        axs[itFu, itSubj].plot(x, density_ran(x), 'r')
        # axs[itFu, itSubj].plot(x, density_reg(x), 'b')
        axs[itFu, itSubj].set_xlim([0, 1])
        axs[itFu, itSubj].set_title("{}, {}, C.I. {:.1f}+/-{:.1f}".format(su, fu, m, s))

# Add benchmarks distributions
n, x, _ = axs[0, 5].hist(temp_datar, bins=n_bins, density=True)
axs[0, 5].plot(x, density_ran(x), 'r')
axs[0, 5].set_title("Random data, C.I. {:.1f}+/-{:.1f}".format(np.mean(temp_datar), np.std(temp_datar)))
n, x, _ = axs[1, 5].hist(temp_datag, bins=n_bins, density=True)
axs[1, 5].plot(x, density_reg(x), 'r')
axs[1, 5].set_title("Regular Hexbins, C.I. {:.1f}+/-{:.1f}".format(np.mean(temp_datag), np.std(temp_datag)))


# Saving plot
plt.savefig(os.path.join(PATH_OUT,'columnar_index_conv_brain_{}_AllSbj_and_benchmark_pdf_random.jpeg'.format(ROI, MASK)), bbox_inches='tight')
plt.savefig(os.path.join(PATH_OUT,'columnar_index_conv_brain_{}_AllSbj_and_benchmark_pdf_random.svg'.format(ROI, MASK)), bbox_inches='tight')
plt.show()
