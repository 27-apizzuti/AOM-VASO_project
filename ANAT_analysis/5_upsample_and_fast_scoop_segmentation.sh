#!/bin/bash
# Upsample T1_weighted image and run the segmentation (FSL fast)
# In ITK determine the scoop to segment before run this script (use activation maps as guide).
# Run for: P02, P03, P04, P05

# Define input
SUBJ=sub-06
thr=4   # scaling factor
myvaso=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/boco
myanat=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/alignment_ANTs
mysegm=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/segmentation_${thr}
T1_weighted=${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_slab
# ------------------------------------------------------------------------------
# Create output folder
if [ ! -d ${mysegm} ]; then
  mkdir -p ${mysegm};
fi
# 1. Upsample > find the paramenters
delta_x=$(3dinfo -di ${myanat}/$T1_weighted.nii)
delta_y=$(3dinfo -dj ${myanat}/$T1_weighted.nii)
delta_z=$(3dinfo -dk ${myanat}/$T1_weighted.nii)
echo "Starting pixel resolution: " $delta_x $delta_y $delta_z
echo "========"

sdelta_x=$(echo "((sqrt($delta_x * $delta_x) / ${thr}))"|bc -l)
sdelta_y=$(echo "((sqrt($delta_y * $delta_y) / ${thr}))"|bc -l)
sdelta_z=$(echo "((sqrt($delta_z * $delta_z) / ${thr}))"|bc -l)
echo "Find upsampling parameters: " $sdelta_x $sdelta_y $sdelta_z
echo "========"

# # 2. Upsample T1 & Scoop > apply the upscale all the dim
echo "Upsample T1_weighted"
echo "========"
3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${mysegm}/${T1_weighted}_scaled_${thr}.nii -input ${myanat}/${T1_weighted}.nii
3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${mysegm}/${SUBJ}_scaled_${thr}_vaso_t1.nii -input ${myvaso}/T1_weighted.nii
3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode NN -overwrite -prefix ${mysegm}/${SUBJ}_scaled_${thr}_scoop.nii -input ${myanat}/scoop.nii.gz

# 4. Segmentation
echo "Masking T1w image"
fslmaths ${mysegm}/${T1_weighted}_scaled_${thr}.nii -mas ${mysegm}/${SUBJ}_scaled_${thr}_scoop.nii ${mysegm}/${T1_weighted}_scaled_${thr}_mask.nii

echo "Running FAST..."
fast -n 3 -o ${mysegm}/${SUBJ}_scaled_${thr} ${mysegm}/${T1_weighted}_scaled_${thr}_mask.nii
LN2_RIMIFY -input ${mysegm}/${SUBJ}_scaled_${thr}_seg.nii.gz -innergm 3 -outergm 1 -gm 2

#######################################

# semi-MANUAL
# wm_thr=7725s
# csf_thr=3000

# fslmaths ${scaled_T1}.nii -mas ${scoop}.nii.gz ${scaled_T1}_mask_${scoop}.nii

# fslmaths ${scaled_T1}_mask_${scoop}.nii -thr $wm_thr -bin -mul 2 hMT_L_${scoop}_segm_wm.nii #wm(2)
# fslmaths ${scaled_T1}_mask_${scoop}.nii -uthr $csf_thr -bin hMT_L_${scoop}_segm_csf.nii #csf(1)
# fslmaths ${scaled_T1}_mask_${scoop}.nii -uthr $wm_thr -thr $csf_thr -bin -mul 3 hMT_L_${scoop}_segm_gm.nii #gm(3)

# fslmaths hMT_L_${scoop}_segm_wm.nii -add hMT_L_${scoop}_segm_csf.nii -add hMT_L_${scoop}_segm_gm.nii hMT_L_${scoop}_segm_wmgmcsf.nii
# rim=hMT_L_${scoop}_segm_wmgmcsf.nii
