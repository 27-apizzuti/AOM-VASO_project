
"""
Created on Sun Oct 24 13:31:42 2021
https://gist.githubusercontent.com/ofgulban/803d4fc0feaf615c7297ebf7e56bd264/raw/8bc2433bda77ac3ee75497bd1fc182151d8d03c1/pyvista_360.py

Rotate BOLD, VASO columnarity map
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
# FILENAME = "D:/Pilot_Exp_VASO/pilotAOM/sub-02/derivatives/anat/patch_flatten/sub-02_seg_rim_4_9_curvature_binned_binz_107_flat_532x532_voronoi_4rendering.nii"
FILENAME = "D:/Pilot_Exp_VASO/pilotAOM/sub-02/derivatives/anat/patch_flatten/sub-02_leftMT_Sphere16radius_BOLD_FDR_VASO_columns_full_depth_UVD_columns_mode_filter_window_count_ratio_binz_107_flat_532x532_voronoi.nii.gz"
OUTDIR = "D:/Pilot_Exp_VASO/pilotAOM/Results/Animations/sub-02/animations/VASO_flat_columnar_map"
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("Output directory: {}\n".format(OUTDIR))

# Data range
MIN, MAX = 0, 1
NR_FRAMES = 50
BACKGROUND = "black"
RESOLUTION = (720, 720)
CMAP = "reds"

# =============================================================================
# Get data
nii = nb.load(FILENAME)
data = nii.get_fdata()
opacity = np.ones(255)
opacity[0] = 0

p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
# data[data < 0] = 0
data *= 255
my_title='VASO Columnar Map'
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
              blending="composite", opacity=opacity, show_scalar_bar=False, opacity_unit_distance=0)
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
