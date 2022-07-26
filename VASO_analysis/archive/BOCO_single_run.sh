#!/bin/bash
# This script performs BOLD-correction on single run.
# # TR-P02:2.4112 / P03: 2.4103 / P04: 2.4771
# Run P04: NORDIC[vaso_analysis/magn_only/magn_phase/standard]
# Run P03: NORDIC[vaso_analysis/magn_phase---vaso_analysis/magn_only]-- REF.[/vaso_analysis/standard] & magn_phasenoNOISE
# Run P02: NORDIC[vaso_analysis/magn_only] -- REF.[/vaso_analysis/standard]

SUBJ=sub-03
TR_SBJ=2.4103

mydata=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/magn_only_noNOISE/moco
mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/${SUBJ}/derivatives/func/AOM/vaso_analysis/magn_only_noNOISE/boco_singleRun

myscript=/mnt/d/Pilot_Exp_VASO/AOM-project

if [ ! -d ${mywork} ]; then
  mkdir -p ${mywork};
fi
echo "No averaging across runs: working at single run"


cnt=0
for run in {0,1,2}
do
echo "Working on run " ${cnt}
mywork_singleRun=${mywork}/run${cnt}

if [ ! -d ${mywork_singleRun} ]; then
  mkdir -p ${mywork_singleRun};
fi

cd ${mywork_singleRun}

echo "Temporal upsampling and shifting happens now"

nulled_sr=Nulled_Basis_${cnt}b.nii
not_nulled_sr=Not_Nulled_Basis_${cnt}a.nii

3dcalc -a ${mydata}/${nulled_sr}'[1..$(2)]' -expr 'a' -prefix Nulled.nii -overwrite
3dcalc -a ${mydata}/${not_nulled_sr}'[0..$(2)]' -expr 'a' -prefix BOLD.nii -overwrite

cp Nulled.nii Nulled_averRuns_halfVol.nii
cp BOLD.nii BOLD_averRuns_halfVol.nii

3dUpsample -overwrite  -datum short -prefix Nulled_interp.nii -n 2 -input Nulled.nii
3dUpsample -overwrite  -datum short -prefix BOLD_interp.nii   -n 2 -input   BOLD.nii
NumVol=`3dinfo -nv BOLD_interp.nii`

3dTcat -overwrite -prefix Nulled_interp.nii Nulled_interp.nii'[0]' Nulled_interp.nii'[0..'`expr $NumVol - 2`']'

# BOLD correction
echo "BOLD correction happens now"                                                        
LN_BOCO -Nulled Nulled_interp.nii -BOLD BOLD_interp.nii
mv VASO_LN.nii VASO_interp_LN.nii

# TR-P02:2.4112 / P03: 2.4103 / P04: 2.4771
echo "I am correcting for the proper TR in the header"
3drefit -TR ${TR_SBJ} BOLD_interp.nii
3drefit -TR ${TR_SBJ} VASO_interp_LN.nii

echo "calculating T1 in EPI space"
NumVol=`3dinfo -nv ${mydata}/${nulled_sr}`
3dcalc -a ${mydata}/${nulled_sr}'[3..'`expr $NumVol - 2`']' -b  ${mydata}/${not_nulled_sr}'[3..'`expr $NumVol - 2`']' -expr 'a+b' -prefix combined.nii -overwrite
3dTstat -cvarinv -prefix T1_weighted.nii -overwrite combined.nii
# rm combined.nii use this to do COPE in BV

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

cnt=$(($cnt+1))
done
