#!/bin/bash
echo "Brain Mask Creation (AFNI)"
# This script is used to create a 3D brain mask for MOCO
# Run 06, 05, 04, 03, 02
SUBJ=sub-06

path_nii=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/sourcedata/session1/NIFTI/func/
path_brainmask=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/brainmask
filename_nii=${SUBJ}_task-aom_acq-3dvasog3_run-01.nii

# Create output folder
if [ ! -d ${path_brainmask} ]; then
  mkdir -p ${path_brainmask};
fi

# Execute
fslmaths ${path_nii}/${filename_nii} -Tmean ${path_brainmask}/mean_run1_VASO.nii.gz
3dAutomask -prefix ${path_brainmask}/mask.nii -peels 3 -dilate 2 -overwrite ${path_brainmask}/mean_run1_VASO.nii.gz