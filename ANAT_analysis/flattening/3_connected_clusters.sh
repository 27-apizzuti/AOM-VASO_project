#!/bin/bash
# Connected cluster on perimeter_chunk
# After Multilaterate we want to be sure that there are no "floated gray matter chunk" in the perimeter chunk file.
# RADIUS: [15, 13, 12, 13, 16]

# Input parameter
SUBJ=sub-06
COND=standard
rad=16
c_p=0
# Parameters established in previous steps
thr=4			# upsampling factor (segmentation)
n_layr=9		# number of layers

# Input folder
path_flat=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/anat/flattening_${thr}_r_${rad}_cp_${c_p}

# Mask the input (we don't want te green perimeter)
fslmaths ${path_flat}/${SUBJ}_perimeter_chunk.nii -uthr 1 ${path_flat}/${SUBJ}_perimeter_chunk_boundary_masked.nii

# Execute connected cluster thresholding
python connected_clusters.py ${path_flat}/${SUBJ}_perimeter_chunk_boundary_masked.nii.gz --cluster_size 100 --connectivity 1 --binarize_labels 1

#LN2_CONNECTED_CLUSTERS -input ${path_flat}/${SUBJ}_perimeter_chunk_mask.nii (as an alternative)
