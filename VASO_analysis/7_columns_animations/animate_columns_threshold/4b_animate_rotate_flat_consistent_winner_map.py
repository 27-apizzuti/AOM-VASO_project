
"""
Created on Sun Oct 24 13:31:42 2021
https://gist.githubusercontent.com/ofgulban/803d4fc0feaf615c7297ebf7e56bd264/raw/8bc2433bda77ac3ee75497bd1fc182151d8d03c1/pyvista_360.py

Rotate BOLD-VASO consistent winner map for a range of columnarity index thresholds
Used for rendering frames as png files.
Run in miniconda prompt (problem with WSL)

@author: apizz
"""

import sys
import os
import numpy as np
import pyvista as pv
import nibabel as nb
from matplotlib.colors import ListedColormap

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02']
FUNC = ['consistent']
CLASS = ['all']
threshold = np.arange(25, 92, 1)
NR_FRAMES = len(threshold)

for itsbj, su in enumerate(SUBJ):

    PATH_IN = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'data', 'consistent_columns', 'polished_columns_2', 'ready-for-animation')

    for fu in FUNC:

        for it, Thr in enumerate(threshold):

            FILENAME = os.path.join(PATH_IN, '{}_winner_map_{}_{}_COL_MASK_plus_curvature_middle_depth_to_the_bottom.nii.gz'.format(su, fu, Thr))

            # For Winner Maps animation
            BACKGROUND = "black"
            RESOLUTION = (720, 720)

            # Prep plotter
            p = pv.Plotter(window_size=RESOLUTION, off_screen=True)

            # Create custome color_map
            red = np.array([1, 0, 0, 1])
            blue = np.array([0, 0.6, 1, 1])
            green = np.array([0, 1, 0, 1])
            purple = np.array([1, 0, 1, 1])
            light_gray = np.array([0.1, 0.1, 0.1, 1])  # 0.1
            dark_gray = np.array([0.3, 0.3, 0.3, 1])  # 0.3
            white = np.array([1, 1, 1, 1])
            black = np.array([0, 0, 0, 0])

            newcolors = np.empty((255, 4))
            newcolors[0:10, :] = black
            newcolors[10:43, :] = red
            newcolors[43:86, :] = blue
            newcolors[86:128, :] = green
            newcolors[128:171, :] = purple
            newcolors[171:214, :] = light_gray
            newcolors[214:230, :] = dark_gray
            newcolors[230:255, :] = white

            # Make the colormap from the listed colors
            CMAP = ListedColormap(newcolors)

            # =============================================================================

            # HARD CODED
            for it_class in CLASS:

                # Get data
                nii = nb.load(FILENAME)
                data = nii.get_fdata()
                opacity = np.ones(255)

                # Output directory
                OUTDIR = os.path.join(STUDY_PATH, 'Results', 'Animations', su, 'animations', 'rot_poli_multiple_threshold_{}_{}'.format(fu, it_class))

                if not os.path.exists(OUTDIR):
                    os.makedirs(OUTDIR)

                if it_class == 'hor':
                    data[data == 1] = 40    # hor, 40
                    data[data == 2] = 240     # vert, 50
                    data[data == 3] = 240     # diag45, 100
                    data[data == 4] = 240     # diag135, 150
                    data[data == 10] = 240
                    my_title = '{} Cortical Columns (C.I.65%)\n Horizontal 0°-180°'.format(fu)

                elif it_class == 'ver':
                    data[data == 1] = 240     # hor, 40
                    data[data == 2] = 50    # vert, 50
                    data[data == 3] = 240     # diag45, 100
                    data[data == 4] = 240     # diag135, 150
                    data[data == 10] = 240
                    my_title = '{} Cortical Columns (C.I.65%)\n Vertical 90°-270°'.format(fu)

                elif it_class == 'diag45':
                    data[data == 1] = 240     # hor, 40
                    data[data == 2] = 240     # vert, 50
                    data[data == 3] = 100   # diag45, 100
                    data[data == 4] = 240     # diag135, 150
                    data[data == 10] = 240
                    my_title = '{} Cortical Columns (C.I.65%)\n Diagonal 45°-225°'.format(fu)

                elif it_class == 'diag135':
                    data[data == 1] = 240     # hor, 40
                    data[data == 2] = 240     # vert, 50
                    data[data == 3] = 240     # diag45, 100
                    data[data == 4] = 150   # diag135, 150
                    data[data == 10] = 240
                    my_title = '{} Cortical Columns (C.I.65%)\n Diagonal 135°-315°'.format(fu)

                else:
                    data[data == 1] = 40     # hor, 40
                    data[data == 2] = 50     # vert, 50
                    data[data == 3] = 100    # diag45, 100
                    data[data == 4] = 150    # diag135, 150
                    data[data == 10] = 240
                    my_title = '{} Cortical Columns (C.I.{}%)'.format(fu, Thr)

                data[data == 5] = 200   # 200 (sulcus)
                data[data == 6] = 220   # 230 (gyri)

                # Adjust opacity
                opacity[0:10] = 0
                opacity[230:255] = 0.01  # create misty
                p.add_volume(data, cmap=CMAP, opacity=opacity, shade=False)
                p.add_text("{}".format(my_title), font="courier")
                p.set_background(BACKGROUND)
                p.remove_scalar_bar()

                # -----------------------------------------------------------------------------
                # Manipulate camera
                p.camera.zoom(1.3)
                # Move camera
                # p.camera.elevation -= 45 / NR_FRAMES
                p.camera.azimuth += 360 / NR_FRAMES * it
                p.camera.azimuth += 360 / NR_FRAMES
                p.camera.azimuth %= 360

                sys.stdout.write("  Frame {}/{} \r".format(it+1, NR_FRAMES))
                sys.stdout.flush()

                p.show(auto_close=False)

                out_name = "frame-{}.png".format(str(it).zfill(3))
                p.screenshot(os.path.join(OUTDIR, out_name))



print("Finished.")
