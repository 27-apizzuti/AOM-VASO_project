"""
Created on Thu Nov  4 16:32:35 2021

@author: apizz
"""

import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
import os
from my_layer_profiles import *

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02']     # , 'sub-03', 'sub-04', 'sub-05', 'sub-06'
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']
MASK = ["BOLD_CV_AVG", "VASO_CV_AVG"]            # "BOLD_CV_AVG", "VASO_CV_AVG", "BOLD_vox", "VASO_vox"
ROI = ['leftMT_Sphere16radius']
n_lay = 3
tag = 'psc'

PATH_OUT = os.path.join(STUDY_PATH, 'Results', 'LayerProfiles')

# my_dpi = 96
# fig1, axs1 = plt.subplots(figsize=(1920/my_dpi, 1080/my_dpi),
#             dpi=my_dpi)
fig1, axs1 = plt.subplots()
# fig1.suptitle('Layers Profiles'.format(MASK))
NPY_FILENAME = 'AllSbj_LayerProfiles.npy'
layer_dict = np.load(os.path.join(PATH_OUT, NPY_FILENAME),
                                  allow_pickle=True).item()

x = np.asarray(layer_dict['layerProfilesBOLD'])
y = np.asarray(layer_dict['layerProfilesVASO'])
x_mean = np.mean(x, axis=0)
y_mean = np.mean(y, axis=0)


for itSbj, si in enumerate(SUBJ):

    for it, fu in enumerate(FUNC):

            idx_layers = np.asarray(range(1, n_lay + 1))


            if it == 0:
                # Plotting: Layer Profiles
                axs1.plot(idx_layers, x_mean*100, linewidth=1, linestyle='-', marker='o', label='{}'.format(fu))
                axs1.set_ylim((0, 3))
                # axs1.set_xlabel("Layers (0=white matter)")
                # axs1.set_ylabel("BOLD Percent Signal Change", color="blue")
                # axs1.set_title("{} Layers Profiles".format(si))
                # axs1.grid(True)
                # plt.yticks(visible=False)
                # axs1[itSbj].legend()
                # axs1[it].hist(idx_layers, layer_dict['binVASO'][itSbj])
            else:
                ax2=axs1.twinx()
                ax2.plot(idx_layers, y_mean*100, linewidth=1, linestyle='-', marker='o', label='{}'.format(fu), color="red")
                ax2.set_ylim(0, 3)
                # ax2.set_xlabel("Layers (0=white matter)")
                # ax2.set_ylabel("VASO Percent Signal Change", color="red")
                # axs1[it].hist(idx_layers, layer_dict['binBOLD'][itSbj])
                # ax2[itSbj].set_title("{} Layers Profiles".format(si))
                # ax2.grid(True)
                # ax2[itSbj].legend()



    fig1.tight_layout()
    fig1.savefig(os.path.join(PATH_OUT,'allSbj_LayerProfiles_{}_mask_{}.svg'.format(ROI[0], MASK)), bbox_inches='tight')
    fig1.show()
