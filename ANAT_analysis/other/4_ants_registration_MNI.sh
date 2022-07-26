#!/bin/bash
# Co-registration visfAtlas (MNI space) to functional space (AOM)
# 
# Step1. ITK-SNAP 3.6 --> run "affine" registration 
#
# Target: sub-04_acq-mp2rage_UNI_reg.nii (raw)
# Moving: MNI152_T1_1mm.nii.gz
# Use default options > save initial_affine_matrix.mat
# 
# Step2. Greedy.exe (ITK-SNAP 3.8) --> catenate trans matrices and reslice segmentation file
#
# Trans. matrices: initial_affine_matrix.mat (affine) + registered_1Warp.nii.gz (MP2RAGE to AOM slab)
# Target: denoised_muncorr.nii // T1w from BOCO (slab)
# Moving: visfAtlas_MNI152_volume.nii.gz

# greedy.exe -d 3 -rf denoised_muncorr.nii -ri LABEL 0.2vox -rm visfAtlas_MNI152_volume.nii.gz visfAtlas_warp_slab_func.nii.gz -r registered_1Warp.nii.gz initial_affine_matrix.mat
greedy.exe -d 3 -rf denoised_muncorr.nii -ri LINEAR -rm MNI152_T1_1mm.nii.gz MNI152_T1_1mm_warp_slab_func.nii.gz -r registered_1Warp.nii.gz initial_affine_matrix.mat