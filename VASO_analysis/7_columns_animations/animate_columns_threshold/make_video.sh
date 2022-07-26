#!/bin/bash
# Compile an MP4 from a folder containing PNGs
PATH_IN=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/consistent_all_65
PATH_OUT=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/NEW_VIDEO_fmedian_fmode

ffmpeg -framerate 10 -i ${PATH_IN}/frame-0%2d.png -vb 20M -c:v libx264 -pix_fmt yuv420p -y ${PATH_OUT}/rot_Columns_consistent_columnarity_65.mp4

# Convert mp4 into a high quality gif
ffmpeg -y -i ${PATH_OUT}/rot_Columns_consistent_columnarity_65.mp4 -vf "fps=10, scale=768:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ${PATH_OUT}/rot_Columns_consistent_columnarity_65.gif

