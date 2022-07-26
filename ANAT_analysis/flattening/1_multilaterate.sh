#!/bin/bash
# Multilaterate script
# Input: -control point 0, -MRI data (T1w, UNI), -Segmentation file (rim), -radius
# NB: Pay attention to the radius input choice: the disk (output) should not hit the boundary of the image

echo "Compute Geodesic Distances from control point 0 and compute UV coordinates (LAYNII)"

SUBJ=sub-04
COND=standard

# Parameters established in previous steps
thr=4			# upsampling factor (segmentation)
n_layr=9		# number of layers
rad=12
c_p=2

# Input folders
path_anat=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/segmentation_${thr}
path_layr=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/layers_${thr}

# Input data
mri_data=${path_anat}/${SUBJ}_acq-mp2rage_UNI_ss_warp_resl_slab_scaled_${thr}_mask.nii.gz
rim_file=${path_anat}/${SUBJ}_scaled_${thr}_seg_rim.nii.gz
midGM_cp0=${path_layr}/${SUBJ}_seg_rim_${thr}_${n_layr}_midGM_equidist_control_point_${c_p}.nii

# Output folder
path_flat=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/flattening_${thr}_r_${rad}_cp_${c_p}

# Create output folder
if [ ! -d ${path_flat} ]; then
  mkdir -p ${path_flat};
fi

# Execute
LN2_MULTILATERATE -rim ${rim_file} -control_points ${midGM_cp0} -radius $rad -norms -output ${path_flat}/${SUBJ}
