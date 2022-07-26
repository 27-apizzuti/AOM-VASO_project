"""
Created on Mon Feb  7 14:21:37 2022
!!! FLAT
Violin plot: column size comparison between BOLD and VASO

@author: apizz
"""
import glob
import numpy as np
import nibabel as nb
import os
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04','sub-05','sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'Columns')
AXIS = ['Horizontal', 'Vertical', 'Diag45', 'Diag135']
PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Columns')
my_dpi = 300
MASK = 'no_mask'

for itSbj, su in enumerate(SUBJ):
    for itCond, cond in enumerate(AXIS):

        for itFunc, fu in enumerate(FUNC):
            if MASK == 'no_mask':
                FILE = "{}_{}_{}_heatmap_no_mask_columns_{}_flat_thick.nii".format(su, ROI[0], cond, fu)
            else:
                FILE = "{}_{}_{}_CV_heatmap_columns_{}_flat_thick.nii".format(su, ROI[0], cond, fu)

            nii = nb.load(os.path.join(PATH_IN, FILE))
            heat_map = nii.get_fdata()
            dims = np.shape(heat_map)
            segm_col = np.zeros(dims)
            segm_col[heat_map > 0.8] = 1

            # # Save segmentation for column polishing
            # out_name = os.path.join(PATH_IN, '{}_{}_{}_CV_heatmap_segm_columns_{}_flat'.format(su, ROI[0], cond, fu))
            # out = nb.Nifti1Image(segm_col, header=nii.header, affine=nii.affine)
            # nb.save(out, out_name)

            # --------------------
            heat_map = heat_map[..., 0]
            flat_map = (heat_map[heat_map > 0]).flatten()
            flat_map_sign = flat_map[flat_map > 0.8]
            print("For {}, {}, percentage of columns with size > .8 {}".format(su, fu, ((len(flat_map_sign))/len(flat_map))*100 ))
            if fu == 'BOLD':
                dataB = flat_map_sign
            else:
                dataV = flat_map_sign

        # Put data into dictionary
        data_plot = {'BOLD': dataB, 'VASO': dataV}
        # Padding with NaN
        maxsize = max([a.size for a in data_plot.values()])
        data_pad = {k:np.pad(v, pad_width=(0,maxsize-v.size,), mode='constant', constant_values=np.nan) for k,v in data_plot.items()}
        df = pd.DataFrame(data_pad)

        fig, ax = plt.subplots()
        sb.violinplot(data=df, scale="count")
        plt.ylim((0,7))
        plt.title('{} {} (cols >.8={}%)'.format(su, cond, ((len(flat_map_sign))/len(flat_map))*100 ))
        fig_filename = "{}_volin_plot_{}_no_mask".format(su, cond)

        # Save figure
        fig.tight_layout()
        plt.savefig(os.path.join(PATH_OUT, "{}.svg".format(fig_filename)),
                bbox_inches='tight', dpi=my_dpi)
        plt.savefig(os.path.join(PATH_OUT, "{}.jpeg".format(fig_filename)),
                bbox_inches='tight', dpi=my_dpi)
        plt.show()
