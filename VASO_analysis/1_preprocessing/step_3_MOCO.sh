#!/bin/bash
# Motion Correction (SPM12)
#

# Define Input
SUBJ=sub-05
path_der_in=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/sourcedata/session1/NIFTI/func/vaso
path_der_out=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/moco
path_brainmask=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/brainmask
myscript=/mnt/d/Pilot_Exp_VASO/AOM-project/VASO_analysis

# ---------------------------------------------------------------------------
echo "Starting MOCO.sh"
echo "Data folder: " ${path_der_in}
echo "Working folder: " ${path_der_out}

# Create output folder
if [ ! -d ${path_der_out} ]; then
  mkdir -p ${path_der_out};
fi

cd ${path_der_out} 	# remain in this folder
cnt=0
for filename in ${path_der_in}/N*.nii   ##### Change with N*.nii with NODIC data; s*.nii with no NORDIC
do
cp $filename ./Basis_${cnt}a.nii

3dTcat -prefix Basis_${cnt}a.nii Basis_${cnt}a.nii'[4..7]' Basis_${cnt}a.nii'[4..$]' -overwrite

cp ./Basis_${cnt}a.nii ./Basis_${cnt}b.nii

3dinfo -nt Basis_${cnt}a.nii >> NT.txt
3dinfo -nt Basis_${cnt}b.nii >> NT.txt
cnt=$(($cnt+1))
echo run $cnt

done
# copy the mask for motion correction
cp ${path_brainmask}/mask.nii .
mv mask.nii moma.nii

# copy the matlab script
cp ${myscript}/mocobatch_VASO_flex.m .
echo "Starting mocobatch_VASO_flex.m (matlab script)"
/mnt/c/'Program Files'/MATLAB/R2020b/bin/matlab.exe -nodesktop -nosplash -r "run mocobatch_VASO_flex.m"
