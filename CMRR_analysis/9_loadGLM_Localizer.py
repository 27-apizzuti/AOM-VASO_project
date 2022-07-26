"""
OPEN LOCALIZER GLM in BV-Axis of Motion (BrainVoyager)
    Load GLM results in BrainVoyager to create .vmp maps

14-05-21

AP [BV22]
# Run for P02, P03, P04, P05, P06
"""
import os

print("Hello!")
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02']

for si in SUBJ:
    PATH_VMR = os.path.join(STUDY_PATH, si, 'derivatives', 'anat', 'alignment_ANTs')
    PATH_VTC = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'loc01', 'BV_GLM')
    docVMR = brainvoyager.open(os.path.join(PATH_VMR, si + '_acq-mp2rage_UNI_ss_warp_resl_slab_reframe256.vmr'))

    if si in ['sub-02', 'sub-05', 'sub-07']:
        vtc_filename = si + '_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_warp_resl_slab_NeuroElf_IDENTITY.vtc'
    else:
        vtc_filename = si + '_task-loc_acq-2depimb3_run-01_SCSTBL_3DMCTS_THPGLMF6c_undist_warp_resl_slab_NeuroElf_IDENTITY.vtc'
    docVMR.link_vtc(os.path.join(PATH_VTC, vtc_filename))

    docVMR.link_protocol(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols', si + '_Pilot_MT_Localizer.prt'))
    docVMR.load_glm(os.path.join(PATH_VTC, si + '_loc.glm'))
