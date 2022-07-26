#!/bin/bash
# This script performs Layers Profile (AFNII, 3dROIstats)
# Run P02, standard, magn_only
# Run P03, standard, magn_only, magn_only_noNOISE
# Run P04, standard, magn_only

SUBJ=sub-03
COND=magn_only_noNOISE

# Input to set for this step (optionally)
# mask_act=0		# (logic) threshold the activation maps
# act_thr=0.01	# threshold the BOLD activation maps (same used for VASO)

# Parameters established in previous steps
thr=4			# upsampling factor (segmentation) 
n_layr=9		# number of layers
thick_thre=0	# (logic) 1.5 to 3cm GM thickness, hard coded in 8_LAYERING.sh
bold_mask=0.01
vaso_mask=0.001

# Folders
mylayr=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/layers_${thr}
mycol=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/columns_${thr}

# Create output folder
mylayr_prof=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/LAYERS_masked

if [ ! -d ${mylayr_prof} ]; then
  mkdir -p ${mylayr_prof};
fi

echo "========"
echo "Get Layers Profiles"

# Working in mydata folder 
cd ${mycol}

# Use significant active voxels
layer_file=${SUBJ}_seg_rim_${thr}_${n_layr}_layers_equidist.nii 
act_fileBOLD=BOLD_${COND}_masked_${bold_mask}_colums_mean.nii
act_fileVASO=VASO_${COND}_masked_${vaso_mask}_colums_mean.nii

# Get Layers Profiles-BOLD
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzmean ${mycol}/${act_fileBOLD} > ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -sigma ${mycol}/${act_fileBOLD} >> ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzvoxels ${mycol}/${act_fileBOLD} >> ${mylayr_prof}/layer_t.dat

WRD=$(head -n 1 ${mylayr_prof}/layer_t.dat|wc -w); for((i=2;i<=$WRD;i=i+2)); do awk '{print $'$i'}' ${mylayr_prof}/layer_t.dat| tr '\n' ' ';echo; done > ${mylayr_prof}/layer.dat

mv ${mylayr_prof}/layer.dat ${mylayr_prof}/BOLD_masked_layers.dat
rm ${mylayr_prof}/layer_t.dat

# Get Layers Profiles-VASO
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzmean ${mycol}/${act_fileVASO} > ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -sigma ${mycol}/${act_fileVASO} >> ${mylayr_prof}/layer_t.dat
3dROIstats -mask ${mylayr}/${layer_file} -1DRformat -quiet -nzvoxels ${mycol}/${act_fileVASO} >> ${mylayr_prof}/layer_t.dat

WRD=$(head -n 1 ${mylayr_prof}/layer_t.dat|wc -w); for((i=2;i<=$WRD;i=i+2)); do awk '{print $'$i'}' ${mylayr_prof}/layer_t.dat| tr '\n' ' ';echo; done > ${mylayr_prof}/layer.dat

mv ${mylayr_prof}/layer.dat ${mylayr_prof}/VASO_masked_layers.dat
rm ${mylayr_prof}/layer_t.dat