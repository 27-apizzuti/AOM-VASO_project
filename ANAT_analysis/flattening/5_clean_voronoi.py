"""
Created on Wed Nov  3 15:56:47 2021

Mask PATH_FLATTEN results in "PATH_IN" folder with a disk when -voronoi flag is used.

@author: apizz
"""
import os, glob
import numpy as np
import nibabel as nb

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
CONDT = ['standard']
ROI = ['leftMT_Sphere16radius']

for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
    os.chdir(PATH_IN)
    for file in glob.glob('*_voronoi.*'):
        print('Working on {}, file {}'.format(su, file))

        nii = nb.load(os.path.join(PATH_IN, file))
        data = nii.get_fdata()
        dims = np.shape(data)
        c = np.indices(dims[0:2], dtype=float)
        centre = dims[0] / 2
        coord_centre = c - centre
        norm = np.linalg.norm(coord_centre, axis=0)
        idx = norm > centre
        data[idx] = 0
        out_name = os.path.join(PATH_IN, file)
        out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
        nb.save(out, out_name)
