#!/bin/bash
# Reslicing (Syn, by ANTs)
#
# Input files: 1. Time series processed, 2. Transformation matrices (/alignment_ANTs folder)
# Check mySource file: it can be distoreted (P02) or undistored (P03, P04)

echo " Co-registration-part III: Reslicing time series ----> Source to Target   [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# P04 P03 P06 (Undistorted, COPE)
SUBJ=sub-06
TASK=loc
RUN=01
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}/alignment_ANTs
myTimeSeries=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}
outfld=${myTimeSeries}/BV_GLM

# Create output folder
if [ ! -d ${outfld} ]; then
  mkdir -p ${outfld};
fi

cd ${mydata}

# Time series resampling
antsApplyTransforms -d 3 -e 3 -i ${myTimeSeries}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c_undist.nii.gz -o ${outfld}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c_undist_warp_resl_slab.nii -r Target_slab.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

# =================
# # P02, P05 (Distorted)
# SUBJ=sub-05
# TASK=loc
# RUN=01
# mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}/alignment_ANTs
# myTimeSeries=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}
# outfld=${myTimeSeries}/BV_GLM
#
# # Create output folder
# if [ ! -d ${outfld} ]; then
#   mkdir -p ${outfld};
# fi
#
# cd ${mydata}
#
# # Time series resampling
# antsApplyTransforms -d 3 -e 3 -i ${myTimeSeries}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c.nii.gz -o ${outfld}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c_warp_resl_slab.nii -r Target_slab.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#
