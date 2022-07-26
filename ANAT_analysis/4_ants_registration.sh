#!/bin/bash
# Non Linear Coregistration (Syn, by ANTs)
#
# Input files: 1. Target, 2. Source 3. initial_matrix_ITK.txt (manual+rigid+affine, by ITK-SNAP) 4. mask.nii around ROI
# No mask option used for P04 and P03 P02 (anat alignment), P05

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS

# 1. Register MP2RAGE to functional AOM_VASO anatomy
# Define Input
SUBJ=sub-06
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat
myTarget=${mydata}/T1w_preparation/denoised_muncorr.nii
mySource=${mydata}/${SUBJ}_acq-mp2rage_UNI_ss_bias_field_corr_edited.nii.gz
myITK=${mydata}/T1w_preparation/
outfld=${mydata}/alignment_ANTs
# ------------------------------------------------------
echo "I expect 2 filed: target file (e.g. high-res T1w from VASO) and a moving (or source) file"
echo " Co-registration-part II: Source to Target ----> Syn [ANTs]"
# Create output folder
if [ ! -d ${outfld} ]; then
  mkdir -p ${outfld};
fi
cd ${outfld}

cp ${mySource} ./Moving.nii
cp ${myTarget} ./Target.nii
cp ${myITK}/initial_matrix_ITK.txt .
# cp ${myITK}/mask.nii.gz

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
# -x mask.nii.gz

antsApplyTransforms -d 3 -i ${mydata}/${SUBJ}_acq-mp2rage_UNI_ss_bias_field_corr_edited.nii.gz -o ${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_slab.nii -r Target.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
antsApplyTransforms -d 3 -i ${mydata}/${SUBJ}_acq-mp2rage_UNI_ss_bias_field_corr_edited.nii.gz -o ${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_wb.nii -r Moving.nii -t registered_1Warp.nii.gz -t registered_0GenericAffine.mat
