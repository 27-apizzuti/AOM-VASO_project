#!/bin/bash

# This script performs BOLD-correction on training (mixed-averaged runs) and test set (single run).

# TR-P02:2.4112 / P03: 2.4103 / P04: 2.4771 / P05: 2.49 / P06: 2.5


SUBJ=(sub-02 sub-03 sub-04 sub-05 sub-06)
TR_SBJ=(2.4112 2.4103 2.4771 2.49 2.5)
PROC=standard

# ====== Start here
cnt=0
for itersubj in ${SUBJ[@]}; do
	echo $itersubj
	echo ${TR_SBJ[$cnt]}

	cnt=$(($cnt+1))
	mywork=/mnt/d/Pilot_Exp_VASO/pilotAOM/$itersubj/derivatives/func/AOM/vaso_analysis/${PROC}/cross_validation
	for subfld in $mywork/run*;
	do
	    echo "$subfld"
		# Create output folder
	    myoutfld=${subfld}/boco
	    echo $myoutfld

		if [ ! -d ${myoutfld} ]; then
		  mkdir -p ${myoutfld};
		fi

		cd ${myoutfld}
	    echo "Temporal upsampling and shifting happens now"
	    3dcalc -a ${subfld}/Nulled_Basis_b.nii.gz'[1..$(2)]' -expr 'a' -prefix Nulled.nii -overwrite
	    3dcalc -a ${subfld}/Not_Nulled_Basis_a.nii.gz'[0..$(2)]' -expr 'a' -prefix BOLD.nii -overwrite

	    cp Nulled.nii Nulled_averRuns_halfVol.nii
	    cp BOLD.nii BOLD_averRuns_halfVol.nii
	    3dUpsample -overwrite  -datum short -prefix Nulled_interp.nii -n 2 -input Nulled.nii
	    3dUpsample -overwrite  -datum short -prefix BOLD_interp.nii   -n 2 -input BOLD.nii
	    NumVol=`3dinfo -nv BOLD_interp.nii`
	    3dTcat -overwrite -prefix Nulled_interp.nii Nulled_interp.nii'[0]' Nulled_interp.nii'[0..'`expr $NumVol - 2`']'

	    # 4. BOLD correction
	    echo "BOLD correction happens now: " $run_a  " " $run_b
	    LN_BOCO -Nulled Nulled_interp.nii -BOLD BOLD_interp.nii
	    mv VASO_LN.nii VASO_interp_LN.nii
	    echo "I am correcting for the proper TR in the header"
	    3drefit -TR ${TR_SBJ[$cnt]} BOLD_interp.nii
	    3drefit -TR ${TR_SBJ[$cnt]} VASO_interp_LN.nii

	    # 5. Statistics
	    # echo "calculating T1 in EPI space"
	    # NumVol=`3dinfo -nv Nulled_Basis_b.nii`
	    # 3dcalc -a Nulled_Basis_b.nii'[3..'`expr $NumVol - 2`']' -b  Not_Nulled_Basis_a.nii'[3..'`expr $NumVol - 2`']' -expr 'a+b' -prefix combined.nii -overwrite
	    # 3dTstat -cvarinv -prefix T1_weighted.nii -overwrite combined.nii
	      
	    # echo "calculating Mean and tSNR maps"
	    # 3dTstat -mean -prefix mean_nulled.nii Nulled.nii -overwrite
	    # 3dTstat -mean -prefix mean_notnulled.nii BOLD.nii -overwrite
	    # 3dTstat  -overwrite -mean  -prefix BOLD.Mean.nii \
	    #     BOLD_interp.nii'[1..$]'
	    # 3dTstat  -overwrite -cvarinv  -prefix BOLD.tSNR.nii \
	    #     BOLD_interp.nii'[1..$]'
	    # 3dTstat  -overwrite -mean  -prefix VASO.Mean.nii \
	    #     VASO_interp_LN.nii'[1..$]'
	    # 3dTstat  -overwrite -cvarinv  -prefix VASO.tSNR.nii \
	    #     VASO_interp_LN.nii'[1..$]'

	    echo "curtosis and skew"
	    LN_SKEW -input BOLD_interp.nii
	    LN_SKEW -input VASO_interp_LN.nii
	    cd $mywork
	    echo "===="
 	done
 done
