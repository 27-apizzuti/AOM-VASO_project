#!/bin/bash
# Run P02, standard, magn_only
# Run P03, standard, magn_only, magn_only_noNOISE
# Run P04, standard, magn_only
# Run P05, P06 standard

SUBJ=sub-06
COND=standard
thr=4

myanat=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/alignment_ANTs
myact=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION
myact_out=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/${COND}/ACTIVATION/scaled_${thr}

# Create output folder
if [ ! -d ${myact_out} ]; then
  mkdir -p ${myact_out};
fi

T1_weighted=${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_slab.nii

# 1. Upsample > find the paramenters

delta_x=$(3dinfo -di ${myanat}/$T1_weighted)
delta_y=$(3dinfo -dj ${myanat}/$T1_weighted)
delta_z=$(3dinfo -dk ${myanat}/$T1_weighted)
echo "Starting pixel resolution: " $delta_x $delta_y $delta_z
echo "========"

sdelta_x=$(echo "((sqrt($delta_x * $delta_x) / ${thr}))"|bc -l)
sdelta_y=$(echo "((sqrt($delta_y * $delta_y) / ${thr}))"|bc -l)
sdelta_z=$(echo "((sqrt($delta_z * $delta_z) / ${thr}))"|bc -l) 
echo "Find upsampling parameters: " $sdelta_x $sdelta_y $sdelta_z

# 3. Upsample Activity > apply the upscale all the dim
cd ${myact}
echo ${myact}
cnt=0
for filename in act_*
do
delta=${filename%.nii} 	
echo "Activation: " $filename
echo "basename: " $delta
echo "========"

3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -overwrite -prefix ${myact_out}/scaled_${thr}_${delta}.nii -input ${myact}/${delta}.nii # upsample

done