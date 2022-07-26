#!/bin/bash
# Downsample random data 

NII=/mnt/c/users/apizz/Desktop/temp_LN2_UVD_FILTER/benchmark_random/sub-02_UV_coordinates_hexbins0.5.nii
OUTPUT_NII=/mnt/c/users/apizz/Desktop/temp_LN2_UVD_FILTER/benchmark_random/sub-02_UV_coordinates_hexbins0.5_downsample.nii
scaling_factor=4

# Downsample to 0.8 mm

delta_x=$(3dinfo -di $NII)
delta_y=$(3dinfo -dj $NII)
delta_z=$(3dinfo -dk $NII)

echo "Starting pixel resolution: " $delta_x $delta_y $delta_z

sdelta_x=$(echo "((sqrt($delta_x * $delta_x) * ${scaling_factor}))"|bc -l)
sdelta_y=$(echo "((sqrt($delta_y * $delta_y) * ${scaling_factor}))"|bc -l)
sdelta_z=$(echo "((sqrt($delta_z * $delta_z) * ${scaling_factor}))"|bc -l)

echo "Find down-sampling parameters: " $sdelta_x $sdelta_y $sdelta_z
echo "$NII"

3dresample -dxyz $sdelta_x $sdelta_y $sdelta_z -rmode Cu -prefix OUTPUT_NII -input NII
--------------------------------------------------
3dresample -dxyz 0.8 0.8 0.8 -input sub-02_UV_coordinates_hexbins0.5_random.nii.gz -prefix test.nii