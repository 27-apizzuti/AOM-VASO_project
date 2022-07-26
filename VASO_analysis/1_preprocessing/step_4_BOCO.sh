#!/bin/bash
# This script performs BOLD-correction on averaged runs.
# 1) Temporal interpolation
# 2) BOLD correction, VASO images generation
# 3) Statistics for quality control
# nb: the script expects two files Not_Nulled_Basis_a.nii and Nulled_Basis_b.nii that are motion corrected with SPM (MOCO.sh output)
# TR-P02:2.4112 / P03: 2.4103 / P04: 2.4771 / P05: 2.49 / P06: 2.5
#
# Define Input
SUBJ=sub-06
TR_SBJ=2.5

mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/moco
mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/standard/boco

myscript=/mnt/d/Pilot_Exp_VASO/AOM-project

echo "Data folder: " ${mydata}
echo "Working folder: " ${mywork}

# Create output folder
if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi

# ---------------------------------------------------------------------------
# Averaging RUNS
echo "Temporal averaging of RUNS"
3dMean -prefix ${mywork}/Nulled_Basis_b.nii ${mydata}/Nulled_Basis_0b.nii ${mydata}/Nulled_Basis_1b.nii ${mydata}/Nulled_Basis_2b.nii -overwrite
3dMean -prefix ${mywork}/Not_Nulled_Basis_a.nii ${mydata}/Not_Nulled_Basis_0a.nii ${mydata}/Not_Nulled_Basis_1a.nii ${mydata}/Not_Nulled_Basis_2a.nii -overwrite

cd ${mywork}
# 1. Nulled and NotNulled separation (half n. vols) and upsampling (back to the orig. n. vols)
echo "Temporal upsampling and shifting happens now"
3dcalc -a Nulled_Basis_b.nii'[1..$(2)]' -expr 'a' -prefix Nulled.nii -overwrite
3dcalc -a Not_Nulled_Basis_a.nii'[0..$(2)]' -expr 'a' -prefix BOLD.nii -overwrite
cp Nulled.nii Nulled_averRuns_halfVol.nii
cp BOLD.nii BOLD_averRuns_halfVol.nii

3dUpsample -overwrite  -datum short -prefix Nulled_interp.nii -n 2 -input Nulled.nii
3dUpsample -overwrite  -datum short -prefix BOLD_interp.nii   -n 2 -input   BOLD.nii
NumVol=`3dinfo -nv BOLD_interp.nii`
3dTcat -overwrite -prefix Nulled_interp.nii Nulled_interp.nii'[0]' Nulled_interp.nii'[0..'`expr $NumVol - 2`']'

# 2. BOLD correction
echo "BOLD correction happens now"
LN_BOCO -Nulled Nulled_interp.nii -BOLD BOLD_interp.nii
mv VASO_LN.nii VASO_interp_LN.nii

echo "I am correcting for the proper TR in the header"
3drefit -TR ${TR_SBJ} BOLD_interp.nii
3drefit -TR ${TR_SBJ} VASO_interp_LN.nii

echo "calculating T1 in EPI space"
NumVol=`3dinfo -nv Nulled_Basis_b.nii`
3dcalc -a Nulled_Basis_b.nii'[3..'`expr $NumVol - 2`']' -b  Not_Nulled_Basis_a.nii'[3..'`expr $NumVol - 2`']' -expr 'a+b' -prefix combined.nii -overwrite
3dTstat -cvarinv -prefix T1_weighted.nii -overwrite combined.nii
# rm combined.nii use this to do COPE in BV

# 3) Quality control
echo "calculating Mean and tSNR maps"
3dTstat -mean -prefix mean_nulled.nii Nulled.nii -overwrite
3dTstat -mean -prefix mean_notnulled.nii BOLD.nii -overwrite
  3dTstat  -overwrite -mean  -prefix BOLD.Mean.nii \
     BOLD_interp.nii'[1..$]'
  3dTstat  -overwrite -cvarinv  -prefix BOLD.tSNR.nii \
     BOLD_interp.nii'[1..$]'
  3dTstat  -overwrite -mean  -prefix VASO.Mean.nii \
     VASO_interp_LN.nii'[1..$]'
  3dTstat  -overwrite -cvarinv  -prefix VASO.tSNR.nii \
     VASO_interp_LN.nii'[1..$]'

echo "curtosis and skew"
LN_SKEW -input BOLD.nii
LN_SKEW -input VASO_interp_LN.nii
