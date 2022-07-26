"""
Created on Tue Feb 22 10:29:54 2022

Evaluate columnar property (benchmark data)

@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import scipy.stats as stats
from scipy.stats import norm
import matplotlib.pyplot as plt


STUDY_PATH = "C:\\Users\\apizz\\Desktop\\temp_LN2_UVD_FILTER"
BENCH_MARK = [os.path.join(STUDY_PATH, "benchmark_random", "sub-02_hexbin_res_0_UVD_columns_mode_filter_window_count_ratio.8_random_res_0.2_fix_hs.nii.gz"),
              os.path.join(STUDY_PATH, "benchmark_hexagon", "sub-02_UV_coordinates_hexbins0_UVD_columns_mode_filter_window_count_ratio.5_aom.nii.gz"),
              os.path.join(STUDY_PATH, "benchmark_hexagon_regular", "sub-02_UV_coordinates_hexbins0_UVD_columns_mode_filter_window_count_ratio.5_aom_modulus.nii.gz")]
FNAME = ["hexagon", "hexagon_regular", "random"]
PATH_OUT = "D:\Pilot_Exp_VASO\pilotAOM\Results\Conv_Columns"

# Prepare plot
my_dpi = 96
fig, axs = plt.subplots(nrows=1, ncols=len(BENCH_MARK), figsize=(1920/my_dpi, 1080/my_dpi),
                    dpi=my_dpi)
n_bins = 50

for it, ben in enumerate(BENCH_MARK):

    nii = nb.load(ben)
    data = nii.get_fdata()
    idx = (data > 0) * (data < 1)
    temp_data = data[idx]

    # Fitting distribution (only random)
    # if it == 0:
    density = stats.gaussian_kde(temp_data)

    m = np.mean(temp_data)
    s = np.std(temp_data)
    print("For {}, mean {:.1f} +/- {:.1f}".format(FNAME[it], m, s))
    n, x, _ = axs[it].hist(temp_data, bins=n_bins, density=True)
    axs[it].plot(x, density(x), 'r')
    axs[it].set_xlim([0, 1])
    axs[it].set_title("{}, C.I. {:.1f}+/-{:.1f}".format(FNAME[it], m, s))

# Saving plot
plt.savefig(os.path.join(PATH_OUT,'columnar_index_conv_brain_benchmark.jpeg'), bbox_inches='tight')
plt.savefig(os.path.join(PATH_OUT,'columnar_index_conv_brain_benchmark.svg'), bbox_inches='tight')
plt.show()
