"""
Created on Thu Nov 11 18:13:58 2021
!!! FLAT
Layers profiles for columns

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

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
n_lay = 100
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Columns')
my_dpi = 96
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
        for FILE_2 in glob.glob('act_allTask_{}_scaled_4_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(fu)):
            print('For {}, loading file {}'.format(su, FILE_2))
        nii2 = nb.load(os.path.join(PATH_IN, FILE_2))
        func_map = nii2.get_fdata()

        # 3) segmentation 4 columns
        os.chdir(PATH_OUT)
        for FILE_3 in glob.glob('{}_{}_heatmap_columns_{}_flat_conn_cluster.nii'.format(su, ROI[0], fu)):
            print('For {}, loading file {}'.format(su, FILE_3))
        nii3 = nb.load(os.path.join(PATH_OUT, FILE_3))
        segm_col = nii3.get_fdata()

        # 4) winner map
        os.chdir(PATH_IN)
        for FILE_4 in glob.glob('{}_{}_CV_{}_winner_map_fix_hd_scaled_4_plus1_binz_*_flat_[0-9][0-9][0-9]x[0-9][0-9][0-9]_voronoi.nii.gz'.format(su, ROI[0], fu)):
            print('Working on {}, file {}'.format(su, FILE_4))
        nii4 = nb.load(os.path.join(PATH_IN, FILE_4))
        winner_map = nii4.get_fdata()

        # %% Processing
        # Loop throught axes of motion and get columns indices
        for itAxis in range(0, 4):
            print(itAxis)
            x = segm_col[..., itAxis]
            n_clust = np.unique(x)[1:]

            # Computing number of rows and cols for sub-plotting
            # n_cols = math.ceil(math.sqrt(len(n_clust)))
            # n_rows = len(n_clust) - n_cols



            for itClust, clust in enumerate(n_clust):
                # Create figure
                fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(1920/my_dpi, 1920/my_dpi), dpi=my_dpi)
                fig.suptitle("Preferred axis: {}".format(itAxis))

                print(itClust, clust)
                idx1 = x == clust

                # Extract fmap values per column
                y = func_map[idx1, :]
                idx2 = ( winner_map[idx1] == (itAxis + 1) ) *1

                # Replace with NaN non-significant voxels
                y[idx2 == 0] = float("NaN")

                # Plotting
                axs[itClust].imshow(y)
                # axs[itClust].colorbar()
                axs[itClust].set_ylabel("Transversal depth")
                axs[itClust].set_ylabel("In plane depth")
                axs[itClust].set_title('Cluster {}'.format(itClust))
            fig.tight_layout()
            fig.savefig(os.path.join(PATH_OUT,'{}_{}_Axis_{}.jpeg'.format(su, fu, itAxis)), bbox_inches='tight')
