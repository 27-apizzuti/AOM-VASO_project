#!/bin/bash
# This script performs Mask Columns according to a threshold applyed to act. maps (LN2_MASK)
# Run only for Standard Processing (P02, P03, P04)
SUBJ=sub-04
COND=magn_only_noNOISE						#magn_only_noNOISE

# Parameters established in previous steps
ncol=300		# number of colums
thr=4			# upsampling factor (segmentation)
n_layr=9		# number of layers
thick_thre=0    # (logic) 1.5 to 3cm GM thickness, hard coded in 8_LAYERING.sh
mask_act=0		# (logic) threshold the activation maps
bold_mask=0.01
vaso_mask=0.005	

# Folders
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION/scaled_${thr}
mycol=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/columns_${thr}

# Files Names
activationB=scaled_${thr}_act_allTask_BOLD.nii
activationV=scaled_${thr}_act_allTask_VASO.nii
columns=${SUBJ}_columns${ncol}.nii

LN2_MASK -scores $mydata/${activationB} -columns ${mycol}/${columns} -mean_thresh $bold_mask -output ${mycol}/BOLD_${COND}_column_mask_${bold_mask}_mean.nii
LN2_MASK -scores $mydata/${activationV} -columns ${mycol}/${columns} -mean_thresh $vaso_mask -output ${mycol}/VASO_${COND}_column_mask_${vaso_mask}_mean.nii

fslmaths ${mydata}/${activationB} -mul ${mycol}/BOLD_${COND}_column_mask_${bold_mask}_mean.nii ${mycol}/BOLD_${COND}_masked_${bold_mask}_colums_mean.nii
fslmaths ${mydata}/${activationV} -mul ${mycol}/VASO_${COND}_column_mask_${vaso_mask}_mean.nii ${mycol}/VASO_${COND}_masked_${vaso_mask}_colums_mean.nii