"""
Created on Sat Jul 17 10:28:35 2021
@author: apizz

Subplot max intensity projection 3x5 for each smoothing option (BOLD, Nulled, VASO) x # subjects

NOTES: We can choose the rest condition we want to use: Flicker or CondFix
"""
import matplotlib.pyplot as plt
import nibabel as nib
import os

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']          # 'sub-02', 'sub-03', 'sub-04', 'sub-05',
CONDT = ['standard']
FUNC = ['BOLD', 'Nulled', 'VASO_LN']
block = ["allTask"]     # "Vertical", "Horizontal", "Diag45", "Diag135"
smooth = [0, 0.8, 1.6]
rest = "Flicker"        # can choose between Flicker or CondFix
# ===========================Execute========================================
pathOUT = os.path.join(STUDY_PATH, 'max_int_projection_figures')

if not os.path.exists(pathOUT):
    os.makedirs(pathOUT)

my_dpi = 96
plt.style.use('dark_background')
my_vmin = [0, 0, 0]
my_vmax = [0.05, 0.02, 0.01]
for smt in range(0, len(smooth)):
    fig, axs = plt.subplots(3, 5, figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    for fu in range(0, len(FUNC)):
        for ax in range(0, len(SUBJ)):
            pathIN = os.path.join(STUDY_PATH, SUBJ[ax], 'derivatives', 'func', 'AOM',
                'vaso_analysis', CONDT[0], 'ACTIVATION_v2', 'mean_blockCond_' + FUNC[fu], 'perc_sign_change', 'max_int_projection')

            smt_suffix = str(smooth[smt]).replace(".", "pt")

            if smooth[smt] == 0:
                nii_filename = 'act_{}_{}_{}_max_int_proj.nii.gz'.format(block[0], rest, FUNC[fu])
            else:
                nii_filename = 'smooth_{}_act_{}_{}_{}_max_int_proj.nii.gz'.format(smt_suffix, block[0], rest, FUNC[fu])

            nii = nib.load(os.path.join(pathIN, nii_filename))

            data = nii.get_fdata()
            data = data[:, ::-1]
            data_trans = data.transpose()
            axs[fu, ax].imshow(data_trans, cmap='inferno', vmin=my_vmin[smt], vmax=my_vmax[smt])

            axs[0, ax].set_title(f"{SUBJ[ax]}")
            axs[fu, ax].set_xticks([])
            axs[fu, ax].set_yticks([])
            axs[fu, 0].set_ylabel(FUNC[fu])
            axs[fu, ax].spines['right'].set_visible(False)
            axs[fu, ax].spines['top'].set_visible(False)
            axs[fu, ax].spines['bottom'].set_visible(False)
            axs[fu, ax].spines['left'].set_visible(False)

    plt.suptitle('Percent Signal Change-Maximum Intensity Projection')
    fig_filename = 'allsubject_smooth_{}_{}_vmin_{}_vmax_{}.png'.format(smt_suffix, rest, my_vmin[smt], my_vmax[smt])

    plt.savefig(os.path.join(pathOUT, fig_filename), bbox_inches='tight', dpi=my_dpi)
    plt.show()



# fig, axs = plt.subplots(1, 5, figsize=(7, 4), constrained_layout=True)
# for ax, FUNC in zip(axs, ['hanning', 'lanczos']):
#     ax.imshow(a, interpolation=interp, cmap='gray')
#     ax.set_title(f"subject='{SUBJ[ax]}'")
