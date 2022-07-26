#!/bin/bash
# This script performs Layers Profile (AFNII, 3dROIstats)
# Run P02, standard, magn_only
# Run P03, standard, magn_only, magn_only_noNOISE
# Run P04, standard, magn_only

SUBJ=sub-04
COND=magn_only_noNOISE

# Input to set for this step (optionally)
mask_act=0		# (logic) threshold the activation maps
act_thr=0.01	# threshold the BOLD activation maps (same used for VASO)

# Parameters established in previous steps
thr=4			# upsampling factor (segmentation) 
n_layr=9		# number of layers
thick_thre=0	# (logic) 1.5 to 3cm GM thickness, hard coded in 8_LAYERING.sh

# Folders
mylayr=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/layers_${thr}
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION/scaled_${thr}
mylayr_prof=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/LAYERS/scaled_${thr}_nlayers_${n_layr}_mask_${mask_act}_thick_${thick_thre}

# Create output folder
if [ ! -d ${mylayr_prof} ]; then
  mkdir -p ${mylayr_prof};
fi

if (( ${thick_thre}==1))
then
	echo "Thickness cortex thresholding applyed"
	layer_file=${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist_mt.nii.gz
	suffix=1
else
	echo "No Thickness cortex thresholding applyed"
	layer_file=${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist.nii
	suffix=0
fi

echo "========"
echo "Get Layers Profiles"

# Working in mydata folder 
cd ${mydata}

# Find significant active voxels BOLD (optionally)
echo "Masking voxels using BOLD activity thresholded"
fslmaths scaled_${thr}_act_allTask_BOLD.nii -thr 0.01 -bin mask_act_BOLD.nii

cnt=0
for filename in scaled_*
do
delta=${filename%.nii} 	
echo "Activation: " $filename
echo "basename: " $delta
echo "========"
# Masking voxels (optionally)
if (( ${mask_act}==1))
then
	fslmaths ${delta}.nii -mas mask_act_BOLD.nii masked_${delta}.nii
	act_file=masked_${delta}.nii
	out_namefile=${delta}_n_${n_layr}_${suffix}_mask_layer
else
	act_file=${delta}.nii 
	out_namefile=${delta}_n_${n_layr}_${suffix}_layer
fi

# Get Layers Profiles
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzmean ${mydata}/${act_file} > ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -sigma ${mydata}/${act_file} >> ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzvoxels ${mydata}/${act_file} >> ${mylayr_prof}/layer_t.dat

WRD=$(head -n 1 ${mylayr_prof}/layer_t.dat|wc -w); for((i=2;i<=$WRD;i=i+2)); do awk '{print $'$i'}' ${mylayr_prof}/layer_t.dat| tr '\n' ' ';echo; done > ${mylayr_prof}/layer.dat

mv ${mylayr_prof}/layer.dat ${mylayr_prof}/${out_namefile}.dat
rm ${mylayr_prof}/layer_t.dat
done