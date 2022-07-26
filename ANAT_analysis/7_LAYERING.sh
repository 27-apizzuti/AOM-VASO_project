#!/bin/bash
# This script compute cortical depths measures (LN2_LAYERS, LayNii)

# Define Input
# SUBJ=(sub-02 sub-03 sub-04 sub-05 sub-06)  # Iterate multiple subjects
SUBJ=(sub-04)

# Input to set for this step
n_layr=9			# number of layers
thick_thre=0		# (logic) 1.5 to 3cm GM thickness, hard coded
# Parameters established in previous steps
thr=4  				# upsampling factor (segmentation)

for itersubj in ${SUBJ[@]}; do
	echo "Working on" $itersubj
	# Folders
	mysegm=/mnt/d/Pilot_Exp_VASO/pilotAOM/${itersubj}/derivatives/anat/segmentation_${thr}
	mylayr=/mnt/d/Pilot_Exp_VASO/pilotAOM/${itersubj}/derivatives/anat/layers_${thr}
	rim=${itersubj}_scaled_${thr}_seg_rim.nii.gz

	# Create output folder
	if [ ! -d ${mylayr} ]; then
	  mkdir -p ${mylayr};
	fi

	# Estimating layers based on rim
	LN2_LAYERS -curvature -thickness -equivol -rim ${mysegm}/$rim -nr_layers ${n_layr} -output ${mylayr}/${itersubj}_seg_rim_${thr}_${n_layr}
	echo "========"
done

	# Uncomment to apply cortical thickness mask [optional, mostly used as quality check]
	# if (( ${thick_thre}==1))
	# then
	# 	echo "Thickness cortex thresholding"
	# 	fslmaths ${mysegm}/${SUBJ}_seg_rim_${thr}_${n_layr}_thickness.nii.gz -uthr 3 -thr 1.5 -bin ${mysegm}/${itersubj}_thick_mask.nii #wm(2)
	# 	fslmaths ${mysegm}/${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist.nii.gz -mas ${mysegm}/${itersubj}_thick_mask.nii ${mysegm}/${itersubj}_seg_rim_${thr}_${n_layr}_layers_equidist_mt.nii.gz

	# 	layer_file=${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist_mt.nii.gz
	# 	suffix=1
	# else
	# 	echo "No Thickness cortex thresholding"
	# 	layer_file=${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist.nii
	# 	suffix=0
	# fi
	# echo "========"
