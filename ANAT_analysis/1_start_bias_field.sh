#!/bin/bash
#
# Apply Bias field correction (SPM12)
# [Input: T1_weighted.nii, "fake anatomy", output of BOCO.sh (standard analysis)]
# NOTE: In the subj/deriv/anat the folder "T1w_preparation" will be created and bias-field corrected image will be stored.
#
# Run for: P04, P03, P02, P05

# Define Input
SUBJ=sub-06
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/boco
mywork=/mnt/d/Pilot_Exp_VASO//pilotAOM/${SUBJ}/derivatives/anat/T1w_preparation
myscript=/mnt/d/Pilot_Exp_VASO/AOM-project/ANAT_analysis
# ------------------------------------------------------
echo " Co-registration-part I:  Target preparation_1/2 ----> Bias Field Correction [SPM] "
echo "Data folder: " ${mydata}
echo "Working folder: " ${mywork}
# Create output folder
if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi
cp ${mydata}/T1_weighted.nii ./uncorr.nii
echo "--------- SPM batch script (matlab)"
/mnt/c/'Program Files'/MATLAB/R2020b/bin/matlab.exe -nodesktop -nosplash -r "run Bias_field_script_job.m"
print('Success.')
