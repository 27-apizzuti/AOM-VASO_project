"""
Created on Mon Nov 15 17:08:04 2021
!!! FLAT
Connected cluster to detect columns

@author: apizz
"""
import numpy as np
import nibabel as nb
import os
from skimage.measure import label

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
ROI = ['leftMT_Sphere16radius']
PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Columns')

thr = 50
c_thr = 10        # nominal res. = 0.05 mm (looking for 0.5 iso mm)
conn = 2

# Execute connected cluster thresholding
for itSbj, su in enumerate(SUBJ):
    for itContr, fu in enumerate(FUNC):
        FILE = '{}_{}_heatmap_columns_{}_flat.nii'.format(su, ROI[0], fu)
        nii1 = nb.load(os.path.join(PATH_IN, FILE))
        columns_map = nii1.get_fdata()
        segm_columns = np.zeros(np.shape(columns_map))
        print(FILE)
        for itCond in range(0, 4):
            data = columns_map[..., itCond]
            data[data < thr] = 0
            data[data > thr] = 1


            # connected clusters
            data = label(data, connectivity=conn)
            labels, counts = np.unique(data, return_counts=True)

            count = 0
            for i, (i_label, i_count) in enumerate(zip(labels[1:], counts[1:])):
                if i_count > c_thr:
                    count = count + 1
                    data[data == i_label] = count
                else:
                    data[data == i_label] = 0
            print("For {}, {}: {} cluster found".format(su, fu, count))
            segm_columns[..., itCond] = data

        out_name = os.path.join(PATH_IN, '{}_{}_heatmap_columns_{}_flat_conn_cluster.nii'.format(su, ROI[0], fu))
        out = nb.Nifti1Image(segm_columns, header=nii1.header, affine=nii1.affine)
        nb.save(out, out_name)
