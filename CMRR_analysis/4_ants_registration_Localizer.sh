#!/bin/bash
# Non Linear Coregistration (Syn, by ANTs)
#
# Input files: 1. Target, 2. Source 3. initial_matrix_ITK.txt (manual+rigid+affine, by ITK-SNAP) 4. mask.nii around ROI
# # No mask option used for P04 and P03, P02
echo "I expect 2 filed: target file (e.g. high-res T1w from VASO) and a moving (or source) file"
echo " Co-registration-part II: Source to Target ----> Syn [ANTs]"

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# 2. Localizer/pRF to functional AOM_VASO (using whole brain MP2RAGE_warped or T1w little slab)
# For P04 no need to do rigid and affine transformation, only Syn (anatomy acquired in the same session).
# Check mySource file: it can be distoreted (P02, P05) or undistored (P03, P04)
SUBJ=sub-06
TASK=loc
RUN=01
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}/alignment_ANTs
myTimeSeriesPath=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/${TASK}${RUN}

#myTarget=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/alignment_ANTs/${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_wb.nii
#myTarget=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/T1w_preparation/denoised_muncorr.nii

mySource=${mydata}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF6c_undist_tmean.nii.gz
myTargetSlab=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/alignment_ANTs/Target.nii

myITK=${mydata}

outfld=${mydata}

cd ${outfld}

cp ${mySource} ./Moving.nii
cp ${myTarget} ./Target.nii
cp ${myTargetSlab} ./Target_slab.nii
cp ${myITK}/initial_matrix_ITK.txt .

# Coregistration done in 2 steps
echo "*****************************************"
echo "************* starting with ANTS ********"
echo "*****************************************"
antsRegistration \
--verbose 1 \
--dimensionality 3 \
--float 1 \
--output [registered_,registered_Warped.nii.gz,registered_InverseWarped.nii.gz] \
--interpolation BSpline[5] \
--use-histogram-matching 0 \
--winsorize-image-intensities [0.005,0.995] \
--transform Rigid[0.05] \
--metric MI[Target.nii,Moving.nii,0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--transform Affine[0.1] \
--metric MI[Target.nii,Moving.nii,0.7,32,Regular,0.1] \
--convergence [1000x500,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox \
--initial-moving-transform initial_matrix_ITK.txt \
--transform SyN[0.1,2,0] \
--metric CC[Target.nii,Moving.nii,1,2] \
--convergence [500x100,1e-6,10] \
--shrink-factors 2x1 \
--smoothing-sigmas 1x0vox
-x mask.nii.gz

# Time series resampling
antsApplyTransforms -d 3 -e 3 -i ${myTimeSeriesPath}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF3c_undist.nii.gz \
-o ${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF3c_undist_warp_resl_slab.nii -r Target_slab.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

antsApplyTransforms -d 3 -e 3 -i ${myTimeSeriesPath}/${SUBJ}_task-${TASK}_acq-2depimb3_run-${RUN}_SCSTBL_3DMCTS_THPGLMF3c_undist.nii.gz \
-o warped_tserie_p02_EPI.nii -r Moving.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

# Resampling
antsApplyTransforms -d 3 -i Moving.nii \
-o ${SUBJ}_Moving_Loc_ss_warp_resl_wb_anat.nii -r Target.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

antsApplyTransforms -d 3 -i Moving.nii \
-o ${SUBJ}_Moving_Loc_ss_warp_resl_wb.nii -r Moving.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

antsApplyTransforms -d 3 -i Moving.nii \
-o ${SUBJ}_Moving_Loc_ss_warp_resl_slab.nii -r Target.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
#===========================================
# P04
# Coregistration done in 2 steps
# echo "*****************************************"
# echo "************* starting with ANTS ********"
# echo "*****************************************"

# antsRegistration \
# --verbose 1 \
# --dimensionality 3 \
# --float 1 \
# --output [registered_,registered_Warped.nii.gz,registered_InverseWarped.nii.gz] \
# --interpolation BSpline[5] \
# --use-histogram-matching 0 \
# --winsorize-image-intensities [0.005,0.995] \
# --initial-moving-transform initial_matrix_ITK.txt \
# --transform SyN[0.1,2,0] \
# --metric CC[Target.nii,Moving.nii,1,2] \
# --convergence [500x100,1e-6,10] \
# --shrink-factors 2x1 \
# --smoothing-sigmas 1x0vox
# # -x mask.nii.gz

# antsApplyTransforms -d 3 -i Moving.nii -o warped_moved.nii -r Moving.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
# antsApplyTransforms -d 3 -i Moving.nii -o warped_moved_EPI.nii -r EPI.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

# # Apply the transformation to the time series Localizer
# antsApplyTransforms -d 3 -e 3 -i sub-03_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_undist.nii.gz -o warped_tserie_EPI.nii -r EPI.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

# # Apply the transformation to the time series pRF 01 and 02
# antsApplyTransforms -d 3 -e 3 -i sub-03_task-prf_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF3c_undist.nii -o warped_tserie_p01_EPI.nii -r EPI.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
# antsApplyTransforms -d 3 -e 3 -i sub-03_task-prf_acq-2depimb3_run-02_SCSTBL_3DMCTS_THPGLMF3c_undist.nii.gz -o warped_tserie_p02_EPI.nii -r EPI.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat

# # # Clean the folder
# # mv r* ${outfld}
# # mv w* ${outfld}

# # mv MP2RAGE.nii ${outfld}
# antsApplyTransforms -d 3 -i warped_ssf03_MP2RAGE.nii -o warped_ssf03_MP2RAGE_reslicedAOM.nii -r EPI.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
# from 65
# --transform Rigid[0.05] \
# --metric CC[Target.nii,Moving.nii,0.7,32,Regular,0.1] \
# --convergence [1000x500,1e-6,10] \
# --shrink-factors 2x1 \
# --smoothing-sigmas 1x0vox \
# --transform Affine[0.1] \
# --metric CC[Target.nii,Moving.nii,0.7,32,Regular,0.1] \
# --convergence [1000x500,1e-6,10] \
# --shrink-factors 2x1 \
# --smoothing-sigmas 1x0vox \
