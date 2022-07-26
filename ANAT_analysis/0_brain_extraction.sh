#!/bin/bash
# This script is used to extract the brain for MP2RAGE anatomy and to create a 3D brainmask
#
# 1. Brain extraction (skull strip) (fsl BET). [Input INV2 from MP2RAGE]
# 2. Apply brain mask to UNI
# 3. Bias field correction (SPM12). [Input: UNI from MP2RAGE]
# 3. Create a 3D brain mask  (3dAutomask AFNII)
#
# Run for: P04, P03, P02, P05, P06

# Define Input
SUBJ=sub-06
anat_inv2=${SUBJ}_acq-mp2rage_inv2.nii   # usually we want to use INV2 to do brain extraction
anat_uni=${SUBJ}_acq-mp2rage_UNI.nii	   # can be UNI or UNI_reg
pathIn=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat
mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/brain_extraction
# ------------------------------------------------------
# Create output folder
if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi

# 1. Brain extraction
bet ${pathIn}/${anat_inv2} ${mywork}/ss_f03_${anat_inv2} -m -R -f 0.03

# 2. Apply brain mask to UNI
fslmaths ${pathIn}/${anat_uni} -mas ${mywork}/ss_f03_${anat_inv2}.gz ${pathIn}/${SUBJ}_acq-mp2rage_UNI_ss.nii

# 3. Bias field correction
cp ${pathIn}/${anat_uni} ./uncorr.nii
/mnt/c/'Program Files'/MATLAB/R2020b/bin/matlab.exe -nodesktop -nosplash -r "run Bias_field_script_job.m"

# 4. 3D Brain mask
3dAutomask -prefix ${pathIn}/T1w_preparation/mask.nii -peels 3 -dilate 2 -overwrite ${pathIn}/T1w_preparation/denoised_muncorr.nii

print("Success.")
