#!/bin/bash
# Apply denoising techinque for Rician Noise (ANTS)
# Run P04, P03, P02, P05

# Define Input
SUBJ=sub-06
mydata=/mnt/d/Pilot_Exp_VASO//pilotAOM/${SUBJ}/derivatives/anat/T1w_preparation
myscript=/mnt/d/Pilot_Exp_VASO/AOM-project/ANAT_analysis
myfile=muncorr.nii
# ------------------------------------------------------
echo " Co-registration-part I:  Target preparation_2/2 ----> DenoiseImage [ANTS, part of registration suite] "
mv ${myscript}/muncorr.nii ${mydata}/muncorr.nii
mv ${myscript}/uncorr_seg8.mat ${mydata}/uncorr_seg8.mat

rm ${myscript}/uncorr.nii
rm ${myscript}/c*uncorr.nii
rm ${myscript}/BiasField_uncorr.nii

# Denoising
DenoiseImage -d 3 -n Rician -i ${mydata}/${myfile} -o ${mydata}/denoised_${myfile}
print('Success.')
