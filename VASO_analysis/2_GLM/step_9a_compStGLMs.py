"""
GLM-Axis of Motion Pilot

    Compute GLM in BrainVoyager for high-res AOM BOLD and VASO fMRI

27-Sep-2021

AP [BV22.2]

"""

import os
print("Hello!")

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07']
COND = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']

for si in SUBJ:
    for co in COND:
        for fu in FUNC:
            PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')
            PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'GLM')
            PATH_OUT = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'GLM', 'ROI')

            docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
            docVMR.link_vtc(os.path.join(PATH_VTC, fu + "_NeuroElf_IDENTITY_fixdim_masked_VOI_conj_bilMT_anat_sphere16radius.vtc"))
            docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols', si + '_Pilot_AOM_run01.prt'))

            docVMR.clear_run_designmatrix()

            docVMR.add_predictor("Flicker")
            docVMR.set_predictor_values_from_condition("Flicker", "Flicker", 1)
            docVMR.apply_hrf_to_predictor("Flicker")

            docVMR.add_predictor("Horizontal")
            docVMR.set_predictor_values_from_condition("Horizontal", "Horizontal", 1)
            docVMR.apply_hrf_to_predictor("Horizontal")

            docVMR.add_predictor("Vertical")
            docVMR.set_predictor_values_from_condition("Vertical", "Vertical", 1)
            docVMR.apply_hrf_to_predictor("Vertical")

            docVMR.add_predictor("Diag45")
            docVMR.set_predictor_values_from_condition("Diag45", "Diag45", 1)
            docVMR.apply_hrf_to_predictor("Diag45")

            docVMR.add_predictor("Diag135")
            docVMR.set_predictor_values_from_condition("Diag135", "Diag135", 1)
            docVMR.apply_hrf_to_predictor("Diag135")

            docVMR.save_run_designmatrix(os.path.join(PATH_OUT, 'designMatrix_' + fu + '.sdm'))
            docVMR.serial_correlation_correction_level = 2

            # ROI-GLM command
            #docVMR.compute_run_glm_for_voi(0, 1, 0)
            docVMR.compute_run_glm()
            docVMR.save_glm(os.path.join(PATH_OUT, si + '_' + co + '_' + fu + 'ROI.glm'))
            docVMR.show_glm()
            #
            docVMR.clear_contrasts()
            docVMR.add_contrast("[Horizontal +1] vs [Flicker -1]")
            docVMR.set_contrast_string("-1 +1 0 0 0")

            docVMR.add_contrast("[Vertical +1] vs [Flicker -1]")
            docVMR.set_contrast_string("-1 0 +1 0 0")

            docVMR.add_contrast("[Diag45 +1] vs [Flicker -1]")
            docVMR.set_contrast_string("-1 0 0 +1 0")

            docVMR.add_contrast("[Diag135 +1] vs [Flicker -1]")
            docVMR.set_contrast_string("-1 0 0 0 +1")

            docVMR.add_contrast("[Horizontal +1] + [Vertical +1] + [Diag45 +1] + [Diag135 +1] vs [Flicker -4]")
            docVMR.set_contrast_string("-4 +1 +1 +1 +1")

            docVMR.show_glm(True)
            docVMR.save_maps(os.path.join(PATH_OUT, '{}_{}_meanRuns_{}_ROI.vmp'.format(si, fu, co)))
