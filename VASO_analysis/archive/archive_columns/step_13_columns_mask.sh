#!/bin/bash
# Mask winner map with column mask based on CI
# !!! FLAT
SUBJ=(sub-02 sub-03 sub-04 sub-05 sub-06)
COND=standard
thr=4
ROI=leftMT_Sphere16radius
thr=75
for itersubj in ${SUBJ[@]}; do
	echo "Working on" $itersubj
	my_pathin_wmap=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/masks_maps/patch_flatten
	my_pathin_mask=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Columns
	my_pathout=${my_pathin_wmap}/mask

	if [ ! -d ${my_pathout} ]; then
		mkdir -p ${my_pathout};
	fi


	# Mask winner map with column mask
	fslmaths ${my_pathin_wmap}/${itersubj}_leftMT_Sphere16radius_BOLD_winner_map_*_voronoi.nii.gz -mas ${my_pathin_mask}/${itersubj}_leftMT_Sphere16radius_BOLD_mask_columns_CI_${thr}.nii ${my_pathout}/${itersubj}_leftMT_Sphere16radius_BOLD_winner_map_CI_${thr}.nii.gz

done
