
"""
Created on Sun Oct 24 13:31:42 2021
https://gist.githubusercontent.com/ofgulban/803d4fc0feaf615c7297ebf7e56bd264/raw/8bc2433bda77ac3ee75497bd1fc182151d8d03c1/pyvista_360.py

Rotate curvature file (anatomy).
Used for rendering frames as png files.

@author: apizz
"""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb
from matplotlib.colors import ListedColormap

# Scalar file (e.g. activtion map or anatomical image)
FILENAME = "D:/Pilot_Exp_VASO/pilotAOM/sub-02/derivatives/anat/flattening_4_r_15_cp_0/curvature_per_chunck_masked_zoomed.nii.gz"
OUTDIR = "D:/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/folded_curvature"

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("Output directory: {}\n".format(OUTDIR))

# Data range
MIN, MAX = 0, 2
NR_FRAMES = 50
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "gray"

# =============================================================================
# Get data
nii = nb.load(FILENAME)
data = nii.get_fdata()
opacity = np.ones(255)
opacity[0] = 0

# Prep plotter
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)

# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data *= 255
my_title='Human Area MT\n Folded Brain Chunk'
sargs = dict(width=0.5, height=0.1, vertical=False,
             position_x=0.05, position_y=0.05,
             font_family="courier",
             title_font_size=22,
             label_font_size=18,
             n_labels=3, fmt="%.0f")
data[:, :, -1] = 0
print(data.shape)
pvdata = pv.wrap(data)
act = p.add_volume(pvdata, cmap=CMAP, scalar_bar_args=sargs,
              blending="composite", opacity=opacity, show_scalar_bar=False, opacity_unit_distance=0, shade=True)
p.set_background(BACKGROUND)
p.add_text("{}".format(my_title), font="courier")

# -----------------------------------------------------------------------------
# Manipulate camera
p.camera.zoom(1.3)
for i in range(NR_FRAMES):
    sys.stdout.write("  Frame {}/{} \r".format(i+1, NR_FRAMES))
    sys.stdout.flush()

    p.show(auto_close=False)

    out_name = "frame-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))

    # Move camera
    # p.camera.elevation -= 45 / NR_FRAMES
    p.camera.azimuth += 360 / NR_FRAMES
    p.camera.azimuth %= 360

print("Finished.")
