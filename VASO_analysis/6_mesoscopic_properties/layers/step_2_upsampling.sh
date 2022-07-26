#!/bin/bash
# Upsample T-maps (unthresholded) and binary masks (CV, BOLDmask etc.) to o.2 iso mm

SUBJ=(sub-02 sub-03 sub-04 sub-05 sub-06)
COND=standard
thr=4
ROI=leftMT_Sphere16radius

for itersubj in ${SUBJ[@]}; do
	echo "Working on" $itersubj
	my_pathin_act=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION
	my_pathin_tmap=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/masks_maps/res_pt8
	my_pathin_wmap=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/masks_maps/res_pt8/maps
	my_pathin_mask=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/masks_maps/res_pt8/masks
	my_pathin_EPI=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/boco
	my_pathout=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/masks_maps/res_pt2

	if [ ! -d ${my_pathout} ]; then
		mkdir -p ${my_pathout};
		mkdir -p ${my_pathout}/masks;
		mkdir -p ${my_pathout}/maps;
	fi

	# 1. Upsample > find the paramenters
	echo ${my_pathin_act}/act_allTask_BOLD.nii
	delta_x=$(3dinfo -di ${my_pathin_act}/act_allTask_BOLD.nii)
	delta_y=$(3dinfo -dj ${my_pathin_act}/act_allTask_BOLD.nii)
	delta_z=$(3dinfo -dk ${my_pathin_act}/act_allTask_BOLD.nii)
	echo "Starting pixel resolution: " $delta_x $delta_y $delta_z
	sdelta_x=$(echo "((sqrt($delta_x * $delta_x) / ${thr}))"|bc -l)
	sdelta_y=$(echo "((sqrt($delta_y * $delta_y) / ${thr}))"|bc -l)
	sdelta_z=$(echo "((sqrt($delta_z * $delta_z) / ${thr}))"|bc -l)
	echo "Find upsampling parameters: " $sdelta_x $sdelta_y $sdelta_z

	# Mask EPI data and upsample it (for pial vein detection)
	fslmaths ${my_pathin_EPI}/BOLD_mean.nii -mas ${my_pathin_tmap}/${itersubj}_${ROI}.nii.gz ${my_pathin_tmap}/BOLD_mean_${ROI}.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/BOLD_mean_${ROI}_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/BOLD_mean_${ROI}.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/${itersubj}_BOLD_mean_scaled_${thr}.nii.gz -input ${my_pathin_EPI}/BOLD_mean.nii

	# Unthresholded t-maps
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/${itersubj}_BOLD_${ROI}_tmaps_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_BOLD_${ROI}_tmaps.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/${itersubj}_VASO_${ROI}_tmaps_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_VASO_${ROI}_tmaps.nii.gz

	# Unthresholded Winner Maps
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_BOLD_winner_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_winner_map.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_VASO_winner_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_winner_map.nii.gz

	# Unthresholded Sensitivity Maps
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_BOLD_sensitivity_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_sensitivity_map.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_VASO_sensitivity_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_sensitivity_map.nii.gz

	# Unthresholded Sensitivity Maps
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_BOLD_specificity_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_specificity_map.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/maps/${itersubj}_${ROI}_VASO_specificity_map_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_specificity_map.nii.gz

	# Mask FDR-BOLDmask, CV-AVG BOLD, CV-AVG VASO
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_BOLD_FDR_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_BOLD_FDR_mask.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_BOLD_CV_AVG_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_CV_BOLD_mask.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_VASO_CV_AVG_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_CV_VASO_mask.nii.gz

	# Mask CV-AVG BOLD only, CV-AVG VASO only, CV-AVG best
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_BOLD_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_BOLD_vox_mask.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_VASO_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_VASO_vox_mask.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/masks/${itersubj}_${ROI}_COMM_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_COMM_vox_mask.nii.gz

done
