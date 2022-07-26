#!/bin/bash
echo "NORDIC evaluation"
# This script is used to create NORDIC residuals and tSNR maps using FSL

SUBJ=sub-05

raw_nii_fld=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/sourcedata/session1/NIFTI/func
nordic_nii_fld=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/NORDIC/output/magn_phase
basename=${SUBJ}_task-aom_acq-3dvasog3_run-0
nordic_bs=MP
#NORDIC_MP_	1.nii

for cnt in {1..4}	# Change number of runs!!!!!
do
# Residuals: Standard - NORDIC	
echo "Residual computation for run" $cnt
#fslmaths ${raw_nii_fld}/${basename}${cnt}.nii -sub ${nordic_nii_fld}/NORDIC_${nordic_bs}_${basename}${cnt}.nii ${nordic_nii_fld}/RES_${nordic_bs}_${basename}${cnt}.nii 
echo "Tsnr computation for run" $cnt
3dTstat -tsnr -prefix ${nordic_nii_fld}/tsnr_${basename}${cnt}.nii ${raw_nii_fld}/${basename}${cnt}.nii 
3dTstat -tsnr -prefix ${nordic_nii_fld}/tsnr_NORDIC_${nordic_bs}_${basename}${cnt}.nii ${nordic_nii_fld}/NORDIC_${nordic_bs}_${basename}${cnt}.nii 

done





