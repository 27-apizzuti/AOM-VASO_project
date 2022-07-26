#!/bin/bash
# Apply median filter 
SUBJ=sub-02

FILE1=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_BOLD_winner_map_COL_MASK.nii.gz
OUT1=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_BOLD_winner_map_COL_MASK_fmedian.nii.gz

FILE2=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_VASO_winner_map_COL_MASK.nii.gz
OUT2=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/${SUBJ}/data/${SUBJ}_leftMT_Sphere16radius_VASO_winner_map_COL_MASK_fmedian.nii.gz
echo "${SUBJ}"

fslmaths ${FILE1} -kernel boxv3 5 5 41 -fmedian ${OUT1}
fslmaths ${FILE2} -kernel boxv3 5 5 41 -fmedian ${OUT2}