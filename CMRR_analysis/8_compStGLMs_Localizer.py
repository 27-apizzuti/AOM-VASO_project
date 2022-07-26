"""
GLM-Axis of Motion (BrainVoyager)

    Compute GLM in BrainVoyager for Localizer (warped to high-res AOM space)

26-07-21

AP [BV22]

# Run for P02, P03, P04, P05, P06
"""
import os

print("Hello!")
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')
    PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'loc01', 'BV_GLM')
    docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))
    if si in ['sub-02', 'sub-05']:
        vtc_filename = si + '_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_warp_resl_slab_NeuroElf_IDENTITY.vtc'
    else:
        vtc_filename = si + '_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_undist_warp_resl_slab_NeuroElf_IDENTITY.vtc'
    docVMR.link_vtc(os.path.join(PATH_VTC, vtc_filename))
    docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols', si + '_Pilot_MT_Localizer.prt'))
    docVMR.clear_run_designmatrix()

    docVMR.add_predictor("Center")
    docVMR.set_predictor_values_from_condition("Center", "Center", 1)
    docVMR.apply_hrf_to_predictor("Center")

    # To create a design matrix using all predictors (BV_GLM_3pred folder)
    # docVMR.create_run_designmatrix_from_protocol(0, 1)

    docVMR.save_run_designmatrix(os.path.join(PATH_VTC, 'designMatrix_loc.sdm'))
    docVMR.serial_correlation_correction_level = 2
    docVMR.compute_run_glm()
    docVMR.show_glm()
    docVMR.save_glm(os.path.join(PATH_VTC, si + '_loc.glm'))
    docVMR.close()
