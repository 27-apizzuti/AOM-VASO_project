#!/bin/bash
# NOTE: This script runs in WSL
FILE1=/mnt/d/Pilot_Exp_VASO/pilotAOM/sub-02/derivatives/anat/patch_flatten/sub-02_seg_rim_4_9_curvature_binned_binz_107_flat_532x532_voronoi.nii
LN2_BORDERIZE -input ${FILE1}
