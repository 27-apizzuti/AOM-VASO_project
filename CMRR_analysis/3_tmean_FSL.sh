#!/bin/bash
# This script is used for compute temporal mean of a time series.

SUBJ=sub-06
TASK=loc
RUN=01
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}
filename=${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c_undist

outfld=${mydata}/alignment_ANTs
# Create output folder
if [ ! -d ${outfld} ]; then
  mkdir -p ${outfld};
fi

# Execute
fslmaths ${mydata}/${filename}.nii.gz -Tmean ${outfld}/${filename}_tmean.nii
