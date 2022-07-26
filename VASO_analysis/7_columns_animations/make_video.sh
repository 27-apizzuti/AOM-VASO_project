#!/bin/bash
# Compile an MP4 from a folder containing PNGs
PATH_IN=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/folded_curvature
PATH_OUT=/mnt/d/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/to-create-video/folded_curv

# ffmpeg -framerate 10 -i ${PATH_IN}/frame-0%2d.png -vb 20M -c:v libx264 -pix_fmt yuv420p -y ${PATH_OUT}/mix_VASO.mp4

# Convert mp4 into a high quality gif
ffmpeg -y -i ${PATH_OUT}/curvature_per_chunck.mp4 -vf "fps=10, scale=768:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ${PATH_OUT}/curvature_per_chunck.gif

