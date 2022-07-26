"""
Created on Sat Jul 17 10:28:35 2021

@author: apizz

Subplot max intensity projection GLM pipeline (BOLD,VASO) x # subjects
"""
import matplotlib.pyplot as plt
import nibabel as nib
import os


STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ['BOLD', 'VASO']

pathOUT = os.path.join(STUDY_PATH, 'max_int_projection_figures', 'GLM')

print("Hello!")

if not os.path.exists(pathOUT):
    os.makedirs(pathOUT)

# Plot parameters
my_dpi = 96
plt.style.use('dark_background')
my_vmax = 5
my_vmin= 0
fig, axs = plt.subplots(2, 5, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)

for fu in range(0, len(FUNC)):
    for ax in range(0, len(SUBJ)):

        pathIN = os.path.join(STUDY_PATH, SUBJ[ax], 'derivatives', 'func', 'AOM',
                                  'vaso_analysis', CONDT[0], 'GLM', 'max_int_projection')

        nii_filename = '{}_meanRuns_noNORDIC_bvbabel_max_int_proj.nii.gz'.format(FUNC[fu])

        nii = nib.load(os.path.join(pathIN, nii_filename))

        data = nii.get_fdata()
        data = data[:, ::-1]
        data_trans = data.transpose()
        axs[fu, ax].imshow(data_trans, cmap='inferno', vmin=my_vmin, vmax=my_vmax)

        axs[0, ax].set_title(f"{SUBJ[ax]}")
        axs[fu, ax].set_xticks([])
        axs[fu, ax].set_yticks([])
        axs[fu, 0].set_ylabel(FUNC[fu])
        axs[fu, ax].spines['right'].set_visible(False)
        axs[fu, ax].spines['top'].set_visible(False)
        axs[fu, ax].spines['bottom'].set_visible(False)
        axs[fu, ax].spines['left'].set_visible(False)

plt.suptitle('T-values maps-Maximum Intensity Projection')
fig_filename = 'allsubject_GLM_tvalue_allTask_Flickering_min_{}_max_{}.png'.format(my_vmin, my_vmax)

plt.savefig(os.path.join(pathOUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
plt.show()
