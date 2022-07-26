"""
Created on Wed Dec 16 09:45:57 2020

This script takes in input:
- Nulled_intemp_VASO_LN.nii, BOLD_intemp.nii (averaged across runs) - output of BOCO
- P02_Pilot_AOM_run01.prt - protocol file

According to the prt file this script separate the different conditions (4 task) associating to each one a rest condition (only the rest interval before it)
Both files result from an average operation.

@author: apizz
"""

import numpy as np
import nibabel as nib
import os

# Define Input
STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-04', 'sub-05']
CONDT = ['standard']
FUNC = ['BOLD_interp', 'VASO_interp_LN']

for si in SUBJ:
    for co in CONDT:
        imgBOLD = nib.load(os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'boco', FUNC[0] + '.nii'))
        imgVASO = nib.load(os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'boco', FUNC[1] + '.nii'))
        pathOUT = os.path.join(STUDY_PATH, si, 'derivatives', 'func', 'AOM', 'vaso_analysis', co, 'ACTIVATION','meanCond')

        if not os.path.exists(pathOUT):
            os.makedirs(pathOUT)

        dataB = imgBOLD.get_fdata()
        dataV = imgVASO.get_fdata()

        f = open(os.path.join(STUDY_PATH, si, 'Protocols', 'Protocols', si + '_Pilot_AOM_run01.prt'), "r")
        content_prt = f.read().split()

        cond = ["CondFix", "Flicker", "Horizontal", "Diag45", "Vertical", "Diag135"]
        lab = np.array([1, 2, 3, 4, 5, 6])

        # ============= Build label_times (nvol, 1) and save cond-specific 4D matrix

        nvol = imgBOLD.shape[-1]
        label_times = np.zeros((nvol, 1))
        indAllTask = []

        for iterCond in range(0, len(cond)): # condition loop
            print("Searching volumes for condition: {}\n" .format(cond[iterCond]))
            index = content_prt.index(cond[iterCond])  # position index of "cond" in content_prt
            n = int(content_prt[index + 1])  # number of time intervals for "cond"
            start_t = index + 2  # start point of the first interval

            for iterTimes in range(0, n):
                end_t = start_t + 1
                val_x = int(content_prt[start_t])-1
                val_y = int(content_prt[end_t])
                label_times[val_x:val_y, 0] = lab[iterCond]
                start_t = start_t + 2

            index = [i for i, x in enumerate(label_times == lab[iterCond]) if x]

            dataB_temp = dataB[:, :, :, index]
            print("Saving 4D matrix BOLD for condition: {}\n" .format(cond[iterCond]))
            imgB_out = nib.Nifti1Image(dataB_temp, affine=imgBOLD.affine)
            outB_name = "myBOLD_{}.nii".format(cond[iterCond])
            nib.save(imgB_out, os.path.join(pathOUT, outB_name))

            dataV_temp = dataV[:, :, :, index]
            print("Saving 4D matrix VASO for condition: {}\n" .format(cond[iterCond]))
            imgV_out = nib.Nifti1Image(dataV_temp, affine=imgVASO.affine)
            outV_name = "myVASO_{}.nii".format(cond[iterCond])
            nib.save(imgV_out, os.path.join(pathOUT, outV_name))
            indAllTask.append(index)

        # ============= Save allTask 4D matrix
        print("Saving 4D matrix BOLD and VASO for all conditions")
        idx = indAllTask[2] + indAllTask[3] + indAllTask[4] + indAllTask[5]
        dataB_temp = dataB[:, :, :, idx]
        imgB_out = nib.Nifti1Image(dataB_temp, affine=imgBOLD.affine)
        outB_name = "myBOLD_AllTask.nii"
        nib.save(imgB_out, os.path.join(pathOUT, outB_name))

        dataV_temp = dataV[:, :, :, idx]
        imgV_out = nib.Nifti1Image(dataV_temp, affine=imgVASO.affine)
        outV_name = "myVASO_AllTask.nii"
        nib.save(imgV_out, os.path.join(pathOUT, outV_name))

        # ============= Find REST cond[1]=Flicker condition-specific (which cond follow a REST?)

        newLabel = np.zeros([nvol, 1])
        index = content_prt.index(cond[1])  # identifico indice di posizione
        n = int(content_prt[index + 1])
        start_t = index + 2

        for iterTimes in range(0, n):
            end_t = start_t + 1
            val_x = int(content_prt[start_t])-1  # flick valore iniziale
            val_y = int(content_prt[end_t])    # flick valore finale
            newLabel[val_x:val_y, 0] = label_times[val_y + 1]  # replace "2flick" with the label of the following cond val_y + 1
            start_t = start_t + 2

        # ============= Extract and save cond-spec flicker time intervals

        for ii in range(2, len(cond)):
            index = [i for i, x in enumerate(newLabel == lab[ii]) if x]
            print("Saving 4D matrix BOLD and VASO for Flicker-{}\n".format(cond[ii]))
            dataB_temp = dataB[:, :, :, index]
            imgB_out = nib.Nifti1Image(dataB_temp, affine=imgBOLD.affine)
            outB_name = "myFlick_BOLD_{}.nii".format(cond[ii])
            nib.save(imgB_out, os.path.join(pathOUT, outB_name))

            dataV_temp = dataV[:, :, :, index]
            imgV_out = nib.Nifti1Image(dataV_temp, affine=imgVASO.affine)
            outV_name = "myFlick_VASO_{}.nii".format(cond[ii])
            nib.save(imgV_out, os.path.join(pathOUT, outV_name))
