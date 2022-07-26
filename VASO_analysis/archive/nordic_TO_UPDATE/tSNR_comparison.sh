#!/bin/bash
# This script performs BOLD-correction on single run.
# # TR-P02:2.4112 / P03: 2.4103 / P04: 2.4771
# Run P04: NORDIC[vaso_analysis/magn_only]
# Run P03: NORDIC[vaso_analysis/magn_phase---vaso_analysis/magn_only] & magn_phase_noNOISE

SUBJ=sub-03


# Average section
mypath=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis
myoutput=${mypath}/tsnr_comp

# Create output folder
if [ ! -d ${myoutput} ]; then
  mkdir -p ${myoutput};
fi

# BOLD
mp_tsnr_bold=${mypath}/magn_phase_noNOISE/boco/BOLD_tSNR.nii
m_tsnr_bold=${mypath}/magn_only/boco/BOLD_tSNR.nii
s_tsnr_bold=${mypath}/standard/boco/BOLD_tSNR.nii

fslmaths ${mp_tsnr_bold} -sub ${s_tsnr_bold} ${myoutput}/mp_noNOISE_s_bold.nii # magnphase - standard
# fslmaths ${m_tsnr_bold} -sub ${s_tsnr_bold} ${myoutput}/m_s_bold.nii	# magn - standard
fslmaths ${m_tsnr_bold} -sub ${mp_tsnr_bold} ${myoutput}/m_mp_noNOISE_bold.nii	# magn - magnphase

# VASO

mp_tsnr_vaso=${mypath}/magn_phase_noNOISE/boco/VASO_interp_LN_tSNR.nii
m_tsnr_vaso=${mypath}/magn_only/boco/VASO_interp_LN_tSNR.nii
s_tsnr_vaso=${mypath}/standard/boco/VASO_interp_LN_tSNR.nii

fslmaths ${mp_tsnr_vaso} -sub ${s_tsnr_vaso} ${myoutput}/mp_noNOISE_s_vaso.nii # magnphase - standard
# fslmaths ${m_tsnr_vaso} -sub ${s_tsnr_vaso} ${myoutput}/m_s_vaso.nii	# magn - standard
fslmaths ${m_tsnr_vaso} -sub ${mp_tsnr_vaso} ${myoutput}/m_mp_noNOISE_vaso.nii	# magn - magnphase