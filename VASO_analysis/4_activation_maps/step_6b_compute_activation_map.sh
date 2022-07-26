#!/bin/bash
# Compute activation map: percent signal change (task-rest/rest) for BOLD and VASO
#

echo "I estimate activity"
SUBJ=sub-06
COND=standard

mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION/meanCond
mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION

echo "Data folder: " ${mydata}
echo "Working folder: " ${mywork}

# Create output folder
if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi

cd ${mydata}

# Temporal mean for each condition
cnt=0

for filename in my*
do
echo $filename
fslmaths $filename -Tmean mean_$filename
# fslmaths $filename -Tmedian mean_$filename
done

# Signal change (activation)
3dcalc -a mean_myFlick_VASO_Vertical.nii  -b mean_myVASO_Vertical.nii -overwrite -expr '(a-b)/a' -prefix ${mywork}/act_Vertical_VASO.nii
3dcalc -a mean_myFlick_BOLD_Vertical.nii  -b mean_myBOLD_Vertical.nii -overwrite -expr '(b-a)/a' -prefix ${mywork}/act_Vertical_BOLD.nii

3dcalc -a mean_myFlick_VASO_Horizontal.nii  -b mean_myVASO_Horizontal.nii -overwrite -expr '(a-b)/a' -prefix ${mywork}/act_Horizontal_VASO.nii
3dcalc -a mean_myFlick_BOLD_Horizontal.nii  -b mean_myBOLD_Horizontal.nii -overwrite -expr '(b-a)/a' -prefix ${mywork}/act_Horizontal_BOLD.nii

3dcalc -a mean_myFlick_VASO_Diag45.nii  -b mean_myVASO_Diag45.nii -overwrite -expr '(a-b)/a' -prefix ${mywork}/act_Diag45_VASO.nii
3dcalc -a mean_myFlick_BOLD_Diag45.nii  -b mean_myBOLD_Diag45.nii -overwrite -expr '(b-a)/a' -prefix ${mywork}/act_Diag45_BOLD.nii

3dcalc -a mean_myFlick_VASO_Diag135.nii  -b mean_myVASO_Diag135.nii -overwrite -expr '(a-b)/a' -prefix ${mywork}/act_Diag135_VASO.nii
3dcalc -a mean_myFlick_BOLD_Diag135.nii  -b mean_myBOLD_Diag135.nii -overwrite -expr '(b-a)/a' -prefix ${mywork}/act_Diag135_BOLD.nii

3dcalc -a mean_myVASO_Flicker.nii  -b mean_myVASO_AllTask.nii -overwrite -expr '(a-b)/a' -prefix ${mywork}/act_allTask_VASO.nii
3dcalc -a mean_myBOLD_Flicker.nii  -b mean_myBOLD_AllTask.nii -overwrite -expr '(b-a)/a' -prefix ${mywork}/act_allTask_BOLD.nii
