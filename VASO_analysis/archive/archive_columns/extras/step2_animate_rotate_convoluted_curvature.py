"""Used in thingsonthings.org LN2_MULTILATERATE blog post."""

import os
import numpy as np
import pyvista as pv
import nibabel as nb
import shutil

# Scalar file (e.g. activtion map or anatomical image)
NR_STEPS = 25
PATH_IN= "D:\\Pilot_Exp_VASO\\pilotAOM\\Results\\Animations\\sub-02\\data\\folded_to_flatten"
FILE1 = os.path.join(PATH_IN, 'step1_curv_binn_{}steps_depth21.nii'.format(NR_STEPS))
OUTDIR = "D:\\Pilot_Exp_VASO\\pilotAOM\\Results\\Animations\\sub-02\\animations\\folded_flat"

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Load data
data = nb.load(FILE1).get_fdata()
# Mirror data
# data = data[::-1, :, :]

nr_frames = 25
MIN, MAX = 0, 2
RESOLUTION = (720, 720)
BACKGROUND = "black"

# Normalize to 0-255
data[data > MAX] = MAX
data = (data - MIN) / (MAX - MIN)
data[data < 0] = 0
data *= 255

# Colorbar
sargs = dict(width=0.5, height=0.1, vertical=False,
             position_x=0.05, position_y=0.05,
             font_family="courier",
             title_font_size=22,
             label_font_size=18,
             n_labels=3, fmt="%.0f")

frame_order = np.arange(nr_frames)
frame_order = np.hstack([frame_order, frame_order[::-1]])

opacity = np.ones(255)
opacity[0] = 0
p = pv.Plotter(window_size=RESOLUTION, off_screen=True)
p.set_background(BACKGROUND)
p.add_text("Human area MT:\nfrom folded to flattened brain chunk",
           font="courier", font_size=16)
for i, j in enumerate(frame_order):
    # Get data and clip it
    temp = np.copy(data[..., j])
    pvdata = pv.wrap(temp)

    act = p.add_volume(pvdata, cmap="gray", scalar_bar_args=sargs,
                 opacity="sigmoid", show_scalar_bar=False, opacity_unit_distance=0, shade=True)

    p.show(auto_close=False)
    # p.camera_position = CAMPOS
    out_name = "frame-{}.png".format(str(i).zfill(3))
    p.screenshot(os.path.join(OUTDIR, out_name))
    p.remove_actor(act)
print("Finished.")
