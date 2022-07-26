#!/bin/bash
# Binary mask inversion
# 
# SUBJ=sub-05
# mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat
# anat=sub-05_acq-mp2rage_UNI_ss_bias_field_corr
# mask=cerebellum_mask_polished.nii.gz
#===========================================

# Invert the mask
# fslmaths ${mydata}/brain_extraction/$mask -add 1 ${mydata}/brain_extraction/bis_${mask}
# fslmaths ${mydata}/brain_extraction/bis_${mask} -uthr 1 ${mydata}/brain_extraction/brain_cerebellum_masked.nii.gz

# rm ${mydata}/bis_${mask}

# # Apply the mask

# fslmaths ${mydata}/${anat}.nii -mul ${mydata}/brain_extraction/brain_cerebellum_masked.nii.gz ${mydata}/${anat}_cereb_masked.nii
#===========================================

# Sum masking
SUBJ=sub-05
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/temp
mask1=sub-05_acq-mp2rage_UNI_ss_bias_field_corr_cereb_masked_labels_white_man_pol_wm_pol_dilated.nii.gz
mask2=sub-05_acq-mp2rage_UNI_ss_bias_field_corr_cereb_masked_labels_greythin.nii.gz

fslmaths ${mydata}/${mask2} -add ${mydata}/${mask1} -uthr 1 ${mydata}/sub-05_acq-mp2rage_UNI_ss_final.nii.gz
#===========================================
# Apply final brain mask
SUBJ=sub-06
mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat
anat=sub-06_acq-mp2rage_UNI_ss
mask=sub-06_acq-mp2rage_UNI_ss_labels_wm_pol_pol2_3_4_5_man_pol.nii

fslmaths ${mydata}/${anat}.nii -mul ${mydata}/hammer_segmentator/${mask} ${mydata}/${anat}_edited.nii