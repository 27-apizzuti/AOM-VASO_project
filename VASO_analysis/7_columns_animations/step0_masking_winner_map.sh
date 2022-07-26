#!/bin/bash
# Mask unthresholded winner map with columnar mask (count_ratio > 65%)
# NOTE: Remember to change input parameters manually for each subject and create output folder
# BINZ=[107,103,109,103,115] BINXY=[532,461,426,461,568]

# Input parameters
SUBJ=sub-02
BINZ=107
BINXY=532
# ---------------------
FILE1=/mnt/d/Pilot_Exp_VASO/pilotAOM/$SUBJ/derivatives/func/AOM/vaso_analysis/standard/masks_maps/patch_flatten/${SUBJ}_leftMT_Sphere16radius_BOLD_winner_map_scaled_4_plus1_binz_${BINZ}_flat_${BINXY}x${BINXY}_voronoi.nii.gz
FILE2=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/masks_maps/patch_flatten/${SUBJ}_leftMT_Sphere16radius_VASO_winner_map_scaled_4_plus1_binz_${BINZ}_flat_${BINXY}x${BINXY}_voronoi.nii.gz

MASK1=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/masks_maps/patch_flatten/${SUBJ}_leftMT_Sphere16radius_BOLD_FDR_BOLD_columnar_mask_thr_65_plus1_binz_${BINZ}_flat_${BINXY}x${BINXY}_voronoi.nii.gz
MASK2=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/masks_maps/patch_flatten/${SUBJ}_leftMT_Sphere16radius_BOLD_FDR_VASO_columnar_mask_thr_65_plus1_binz_${BINZ}_flat_${BINXY}x${BINXY}_voronoi.nii.gz

OUT1=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_BOLD_winner_map_COL_MASK.nii.gz
OUT2=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_VASO_winner_map_COL_MASK.nii.gz

fslmaths ${FILE1} -mas ${MASK1} ${OUT1}
fslmaths ${FILE2} -mas ${MASK2} ${OUT2}
