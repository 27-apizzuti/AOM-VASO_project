"""
GLM-Axis of Motion Pilot-Cross Validation (Brainvoyager)
Works for both single run and leave one run out.
    Compute GLM in BrainVoyager for high-res AOM fMRI for
    BOLD and VASO respectivly (BOCO-s ouput)

13-05-21

AP [BV22]
# P02, P03, P04
"""

import os
from glob import glob

print("Hello!")

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07']
COND = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')

    for co in COND:
        PATH_SBJ = os.path.join(STUDY_PATH, si, 'derivatives', 'func',
                                'AOM', 'vaso_analysis', co, 'cross_validation')
        SUBFLD = glob(os.path.join(PATH_SBJ, "run*", ""))
        for sbf in SUBFLD:

            for fu in FUNC:
                print("Working on {} {} {}".format(si, sbf, fu))
                PATH_VTC = os.path.join(PATH_SBJ, sbf, 'GLM')
                PATH_OUT = os.path.join(PATH_VTC, 'ROI')

                if not os.path.exists(PATH_OUT):
                    os.mkdir(PATH_OUT)

                docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
                docVMR.link_vtc(os.path.join(PATH_VTC, fu + "_bvbabel_bvbabel_masked_VOI_conj_bilMT_anat_sphere16radius.vtc"))
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

                docVMR.compute_run_glm()
                docVMR.show_glm()
                docVMR.save_glm(os.path.join(PATH_OUT, si + '_' + co + '_' + fu + '.glm'))

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
                docVMR.close()
print("Done.")
