"""
Created on Wed Nov 17 11:04:50 2021

Global columnarity index

@author: apizz
"""

import glob
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from my_layer_profiles import *
import math
from copy import copy
import pandas as pd

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
n_lay = 3

for itSbj, su in enumerate(SUBJ):
    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')

    # %% Loading input files
    # 1) Metric file
    os.chdir(PATH_IN)
    for FILE_1 in glob.glob('{}_seg_rim_4_9_metric_equivol_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.*'.format(su)):
        print('For {}, loading file {}'.format(su, FILE_1))
    nii1 = nb.load(os.path.join(PATH_IN, FILE_1))
    metrics_map = nii1.get_fdata()
    dims = np.shape(metrics_map)
    lay = my_layer_profiles(metrics_map, n_lay)
    lay = np.reshape(lay, dims)
    os.chdir(PATH_IN)

    for itFunc, fu in enumerate(FUNC):

        # 2) Map (e.g. percent signal change map) /// can be changed in the future
        os.chdir(PATH_IN)
        for FILE_2 in glob.glob('{}_{}_CV_{}_t_map_fix_hd_scaled_4_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(su, ROI[0], fu)):
            print('For {}, loading file {}'.format(su, FILE_2))
        nii2 = nb.load(os.path.join(PATH_IN, FILE_2))
        func_map = nii2.get_fdata()

        psc_deep = copy(func_map)
        psc_sup = copy(func_map)

        # 4) winner map
        os.chdir(PATH_IN)
        for FILE_4 in glob.glob('{}_{}_CV_{}_winner_map_fix_hd_scaled_4_plus1_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(su, ROI[0], fu)):
            print('Working on {}, file {}'.format(su, FILE_4))
        nii4 = nb.load(os.path.join(PATH_IN, FILE_4))
        winner_map = nii4.get_fdata()
        winner_map[winner_map > 0] = 1
        dims = np.shape(winner_map)

        # Create a mask
        act_mask = np.zeros(dims)
        max_val = np.nanmax(winner_map, axis=2)
        act_mask[max_val == 1, :] = 1

        out_name = os.path.join(PATH_IN, '{}_{}_act_mask_{}_flat'.format(su, ROI[0], fu))
        out = nb.Nifti1Image(act_mask, header=nii2.header, affine=nii2.affine)
        nb.save(out, out_name)

        # Compute winner map for all voxels


        # # Find values for deep lay
        # idx_deep = lay == 1
        # idx_deep = np.reshape(idx_deep, dims)

        # idx_deep = np.array(act_mask * idx_deep, dtype=bool)

        # psc_deep[idx_deep == 0] = np.nan
        # deep = np.nanmean(psc_deep, axis=2)

        # idx_nan = np.isnan(deep) * 1
        # idx_not_nan = idx_nan == 0
        # x = deep[idx_not_nan]
        # # x = deep[deep != np.nan]

        # # Find values for superficial lay
        # idx_sup = lay == n_lay
        # idx_sup = np.reshape(idx_sup, dims)

        # idx_sup = np.array(act_mask * idx_sup, dtype=bool)

        # psc_sup[idx_sup == 0] = np.nan
        # sup = np.nanmean(psc_sup, axis=2)
        # y = sup[idx_not_nan]

        # # //// correlation within columns
        # # get empirical correlation between deep and superficial grid points
        # vecCorrCol = np.corrcoef(x, y)
        # print("For {}, {}, correlation = {}".format(su, fu, vecCorrCol[0, 1]))

        # Scatter plot
        # plt.scatter(x, y)
