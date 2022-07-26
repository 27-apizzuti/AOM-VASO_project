
"""
Created on Sun Oct 24 13:31:42 2021
https://gist.githubusercontent.com/ofgulban/803d4fc0feaf615c7297ebf7e56bd264/raw/8bc2433bda77ac3ee75497bd1fc182151d8d03c1/pyvista_360.py

Used for rendering frames as png files.

@author: apizz
"""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb

# FILENAME = "/mnt/d/Pilot_Exp_VASO/pilotAOM/sub-03/derivatives/anat/flattening_4/sub-03_seg_rim_4_9_curvature_binned_FLAT_flat_200x200_voronoi.nii"
# OUTDIR = "/mnt/d/Pilot_Exp_VASO/pilotAOM/sub-03/derivatives/anat/flattening_4/rotation"
FILENAME = "D:\\Pilot_Exp_VASO\\pilotAOM\\sub-03\\derivatives\\anat\\flattening_4\\sub-03_seg_rim_4_9_curvature_binned_FLAT_flat_200x200_voronoi.nii"
OUTDIR = "D:\\Pilot_Exp_VASO\\pilotAOM\\sub-03\\derivatives\\anat\\flattening_4\\rotation"

# Data range
MIN, MAX = 0, 2
NR_FRAMES = 24 * 8
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
# Get data
nii = nb.load(FILENAME)
data = nii.get_fdata()

# Mirror data
data = data[::-1, :, :]

# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data[data < 0] = 0
data *= 255

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
opacity = np.ones(255)
opacity[0] = 0
p.add_volume(data, cmap="gray", opacity=opacity, blending="composite",
             opacity_unit_distance=0)
p.set_background(BACKGROUND)
p.remove_scalar_bar()
p.add_text("Cakeplot", font="courier")

# -----------------------------------------------------------------------------
# Manipulate camera
p.camera.elevation += 10
p.camera.zoom(1.3)
for i in range(NR_FRAMES):
    sys.stdout.write("  Frame {}/{} \r".format(i+1, NR_FRAMES))
    sys.stdout.flush()

    p.show(auto_close=False)

    out_name = "frame-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))

    # Move camera
    p.camera.azimuth += 360 / NR_FRAMES
    p.camera.azimuth %= 360

print("Finished.")
