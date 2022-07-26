"""
Created on Wed Nov  3 15:56:47 2021

Mask PATH_FLATTEN results with a disk when -voronoi flag is used.

@author: apizz
"""
import os, glob
import numpy as np
import nibabel as nb

STUDY_PATH = "D:/Pilot_Exp_VASO/pilotAOM/"
SUBJ = ['sub-02']
RADIUS = [15]
CONDT = ['standard']
ROI = ['leftMT_Sphere16radius']
OUTNAME = 'sub-02_seg_rim_4_9_curvature_binned_binz_107_flat_532x532_voronoi_4rendering.nii'
for iterSbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
    FILE = 'sub-02_seg_rim_4_9_curvature_binned_binz_107_flat_532x532_voronoi.nii'

    nii = nb.load(os.path.join(PATH_IN, FILE))
    data = nii.get_fdata()
    dims = np.shape(data)
    c = np.indices(dims[0:2], dtype=float)
    centre = dims[0] / 2
    coord_centre = c - centre
    norm = np.linalg.norm(coord_centre, axis=0)
    idx = norm > (centre-1.5)
    data[idx] = 0
    out_name = os.path.join(PATH_IN, OUTNAME)
    out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
    nb.save(out, out_name)
