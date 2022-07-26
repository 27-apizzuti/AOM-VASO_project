#!/bin/bash
# Upsample T-map (AVG, CV-AVG) and Percent Signal Change

#fslmaths act_allTask_BOLD.nii -mas sub-02_leftMT_Sphere16radius_CV_VASO_BOLDmask_mask.nii.gz act_allTask_BOLD_masked.nii

SUBJ=(sub-06)
COND=standard
thr=4
ROI=leftMT_Sphere16radius

for itersubj in ${SUBJ[@]}; do
	echo "Working on" $itersubj
	my_pathin_act=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION
	my_pathin_tmap=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/layers_columns/res_pt8/t_maps
	my_pathin_wmap=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/layers_columns/res_pt8/winner_maps
	my_pathin_mask=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/layers_columns/res_pt8
	my_pathin_EPI=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/boco
	my_pathout=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${COND}/layers_columns/res_pt2

	if [ ! -d ${my_pathout} ]; then
		mkdir -p ${my_pathout};
		mkdir -p ${my_pathout}/t_maps;
		mkdir -p ${my_pathout}/psc;
		mkdir -p ${my_pathout}/winner_maps;

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

	# Mask EPI data and upsample it
	fslmaths ${my_pathin_EPI}/BOLD_mean.nii -mas ${my_pathin_mask}/${itersubj}_${ROI}_mask_fix_hd.nii.gz ${my_pathin_mask}/BOLD_mean_${ROI}.nii.gz
	3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/BOLD_mean_${ROI}_scaled_${thr}.nii.gz -input ${my_pathin_mask}/BOLD_mean_${ROI}.nii.gz

	# # Percent signal change maps (no threshold)
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/psc/act_allTask_BOLD_scaled_${thr}.nii.gz -input ${my_pathin_act}/act_allTask_BOLD.nii
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/psc/act_allTask_VASO_scaled_${thr}.nii.gz -input ${my_pathin_act}/act_allTask_VASO.nii
	#
	# # AVG t-map (FDR-BOLDmask)
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_BOLD_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_BOLD_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_VASO_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_VASO_BOLDmask_t_map_fix_hd.nii.gz
	#
	# # CV AVG t-map
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_CV_BOLD_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_CV_BOLD_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_CV_VASO_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_CV_VASO_BOLDmask_t_map_fix_hd.nii.gz
	#
	# Mask FDR-BOLDmask, CV-AVG BOLD, CV-AVG VASO
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_mask_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_mask_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_BOLD_FDR_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_BOLD_FDR_mask.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_BOLD_CV_AVG_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_CV_BOLD_mask.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_VASO_CV_AVG_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_CV_VASO_mask.nii.gz
	#
	# # Mask CV-AVG BOLD only, CV-AVG VASO only, CV-AVG best
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_BOLD_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_BOLD_vox_mask.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_VASO_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_VASO_vox_mask.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/${itersubj}_${ROI}_COMM_vox_mask_scaled_${thr}.nii.gz -input ${my_pathin_mask}/${itersubj}_${ROI}_COMM_vox_mask.nii.gz
	#
	# # Winner Maps
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_BOLD_winner_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_BOLD_winner_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_VASO_winner_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_VASO_BOLDmask_winner_map_fix_hd.nii.gz
	#
	# # Sensitivity Maps
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_BOLD_sensitivity_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_BOLD_sensitivity_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_VASO_sensitivity_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_VASO_BOLDmask_sensitivity_map_fix_hd.nii.gz
	#
	# # Sensitivity Maps
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_BOLD_specificity_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_BOLD_specificity_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_CV_VASO_specificity_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_CV_VASO_BOLDmask_specificity_map_fix_hd.nii.gz

	# # Original t-Maps
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_BOLD_horizontal_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_BOLD_horizontal_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_BOLD_vertical_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_BOLD_vertical_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_BOLD_diag45_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_BOLD_diag45_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_BOLD_diag135_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_BOLD_diag135_t_map_fix_hd.nii.gz

	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_VASO_horizontal_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_VASO_horizontal_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_VASO_vertical_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_VASO_vertical_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_VASO_diag45_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_VASO_diag45_t_map_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/t_maps/${itersubj}_${ROI}_VASO_diag135_t_map_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_tmap}/${itersubj}_${ROI}_VASO_diag135_t_map_fix_hd.nii.gz

	# Original t-Maps
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_BOLD_winner_map_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_winner_map_unthreshold_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_BOLD_specificity_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_specificity_unthreshold_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_BOLD_sensitivity_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_BOLD_sensitivity_unthreshold_fix_hd.nii.gz

	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_VASO_winner_map_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_winner_map_unthreshold_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_VASO_specificity_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_specificity_unthreshold_fix_hd.nii.gz
	# 3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${my_pathout}/winner_maps/${itersubj}_${ROI}_VASO_sensitivity_unthreshold_fix_hd_scaled_${thr}.nii.gz -input ${my_pathin_wmap}/${itersubj}_${ROI}_VASO_sensitivity_unthreshold_fix_hd.nii.gz


done
