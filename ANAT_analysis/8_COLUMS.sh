#!/bin/bash
# This script performs columnar parcelation (LN2_COLUMNS, LayNii)
# Optional, used to inspect layer profiles

SUBJ=sub-04
ncol=300		# number of colums

# Parameters established in previous steps
thr=4			# upsampling factor (segmentation)
n_layr=9		# number of layers
thick_thre=0    # (logic) 1.5 to 3cm GM thickness, hard coded in 8_LAYERING.sh

# Folders
mysegm=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/segmentation_${thr}
mylayr=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/segmentation_${thr}
mycol=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/colums_${thr}

# Create output folder
if [ ! -d ${mycol} ]; then
  mkdir -p ${mycol};
fi

# Computing Columns
rim=${SUBJ}_scaled_${thr}_seg_rim.nii.gz
rim_midgm=${SUBJ}_seg_rim_${thr}_${n_layr}_midGM_equidist.nii

LN2_COLUMNS -rim ${mysegm}/${rim} -midgm ${mylayr}/${rim_midgm} -nr_columns ${ncol} -output ${mycol}/${SUBJ}
