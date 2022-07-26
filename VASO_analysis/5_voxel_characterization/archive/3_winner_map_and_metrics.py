"""
Created on Tue Jul 27 10:54:24 2021

    Winner Maps, Preference Maps and Voxel Characterization

    1. Read VMP (_meanRuns_noNORDIC_ROI_sub-02_leftMT_Sphere16radius.vmp)
    2. Voxels selection using q(FDR) = 0.05 from t-values: 'All Conditions' vs Flicker
    3. Compute Winner Maps (max operator)-map1
    4. Compute Sensitivity (t-values euclidian norm)-map2
    5. Compute Specificity [1-div=1-arcsen( dot(x,y)/norm(x)norm(y) )] /67.5 (max angle possible)-map3
    6. Save new VMP (3 maps) (into input folder)
    7. Save dictionary 'Tuning curves data' as .npy (into input folder)

INPUT: VMP
OUTPUT: VMP and .npy

NOTE:
    Maps oder in .vmp: 1) Horizontal, 2) Vertical 3) Diag45 4) Diag135 5) All Conditions
    Multiple subjects possible
    Multiple ROI
OPTIONS:
    VASO_BOLD_MASK=True BOLD-VOXELS will be used for VASO

@author: apizz

"""

import os
import numpy as np
import bvbabel
from copy import copy

STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
# SUBJ = ["sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]
SUBJ = ["sub-02"]
CONDT = ['standard']
FUNC = ["BOLD_interp", "VASO_interp_LN"]  # Always put BOLD first , "VASO"
ROI_NAME = ["leftMT_Sphere16radius", "rightMT_Sphere16radius"]
q = 0.05
tag = 'c_thr_0'
VASO_BOLD_MASK = False
out_suffix = ""

# ============================================================================
for su in SUBJ:
    PATH_VMP = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                                    'vaso_analysis', CONDT[0], 'GLM', 'ROI')
    for roi in ROI_NAME:
        for fu in FUNC:
            print("Processing {} {} ROI {}".format(fu, su, roi))

            FILENAME_VMP = '{}_{}_meanRuns_{}_ROI_{}_{}.vmp'.format(su, fu, CONDT[0], roi, tag)

            # Read VMP
            IN_FILE = os.path.join(PATH_VMP, FILENAME_VMP)
            header, data = bvbabel.vmp.read_vmp(IN_FILE)
            print(data.shape)
            n_maps = header['NrOfSubMaps']

            # -------------------- unthresholded
            # # Extract FDR threshold from Map #5
            # pos = np.round(header['Map'][4]['FDRTableInfo'][:, 0], decimals=3, out=None) == q
            # fdr_thres = header['Map'][4]['FDRTableInfo'][pos, 1]
            #
            # # In case we want to use BOLD mask
            # if fu == "VASO_interp_LN":
            #     data *= -1                                   # flip VASO sign
            #     if VASO_BOLD_MASK:                            # To use previous vox_idx from BOLD
            #         out_suffix = "_BOLDMASK"
            #     else:
            #         out_suffix = ""
            #         vox_idx = data[:, :, :, 6] > fdr_thres    # Find significant vox_idx from Map #7
            # else:                                             # BOLD data
            #     out_suffix = ""
            #     vox_idx = data[:, :, :, 6] > fdr_thres        # Find significant vox_idx from Map #7
            # -------------------- unthresholded

            # Create 4D matrix of significant t-values
            vox_idx = data[:, :, :, 5] > 0                      # find indices on the ROI binary mask
            temp = np.zeros(data.shape[0:3] + (4,))
            if fu == "VASO_interp_LN":
                data *= -1

            for iterCond in range(0, 4):
                temp[vox_idx, iterCond] = data[vox_idx, iterCond]

            # Get values of the significant voxels
            vox_tvalue = temp[vox_idx, :]

            # Compute Winner/Preference Map
            vox_label = np.argmax(vox_tvalue, axis=-1) + 1

            # Compute Metric #1: Norm (Euclidian Distance)-Sensitivity
            vox_norm = np.linalg.norm(vox_tvalue, ord=None, axis=1, keepdims=False)

            # Compute Metric #2: Divergence-Specificity
            # NOTE: Span [0-270/4D space] --> normalized into [0-1]
            t_asc = np.sort(vox_tvalue, axis=1)
            v = [0, 0, 0, 1]              # reference axis (winning)
            vox_div = np.zeros([t_asc.shape[0]])

            for iterVox in range(0, t_asc.shape[0]):
                u = t_asc[iterVox, :]
                c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) # -> cosine of the angle
                angle = np.arccos(np.clip(c, -1, 1))                # -> radiants
                angle_degree = angle * 180 / np.pi                  # -> degree
                if angle_degree < 0:
                    print("Vectors: {}, {}".format(u, v))
                # vox_div[iterVox] = angle_degree / (270 / 4)         # -> normalized
                vox_div[iterVox] = angle_degree / 180
                vox_div[iterVox] = 1 - vox_div[iterVox]             # -> inverted
                if vox_div[iterVox] < 0:
                    print("Vectors: {}, {}; spec. {}, angle: {}".format(u, v, vox_div[iterVox], angle_degree))

            # %% Put back the winner map into 3D
            new_vmp_data = np.zeros(data.shape[0:3] + (4,))
            new_vmp_data[:,:,:, 0] = data[:, :, :, 4]
            new_vmp_data[vox_idx, 1] = vox_label
            new_vmp_data[vox_idx, 2] = vox_norm
            new_vmp_data[vox_idx, 3] = vox_div
            # new_vmp_data = new_vmp_data.astype(np.float32)

            new_vmp_header = copy(header)
            new_vmp_header['NrOfSubMaps'] = 4
            new_vmp_header["Map"] = new_vmp_header["Map"][0:4]

            # All Cond vs Flicker map
            new_vmp_header["Map"][0]["MapName"] = "All Conditions vs Flicker"
            new_vmp_header["Map"][0]["NrOfUsedVoxels"] = header["Map"][4]["NrOfUsedVoxels"]
            new_vmp_header["Map"][0]["EnableClusterSizeThreshold"] = header["Map"][4]["EnableClusterSizeThreshold"]
            new_vmp_header["Map"][0]["ShowPosNegValues"] = header["Map"][4]["ShowPosNegValues"]
            new_vmp_header["Map"][0]["UpperThreshold"] = header["Map"][4]["UpperThreshold"]
            new_vmp_header["Map"][0]["MapThreshold"] = header["Map"][4]["MapThreshold"]
            new_vmp_header["Map"][0]["LUTFileName"] = header["Map"][4]["LUTFileName"]

            # Winner map
            new_vmp_header["Map"][1]["MapName"] = "Winner Map"
            new_vmp_header["Map"][1]["NrOfUsedVoxels"] = vox_label.size
            new_vmp_header["Map"][1]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][1]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][1]["UpperThreshold"] = np.max(vox_label)
            new_vmp_header["Map"][1]["MapThreshold"] = np.min(vox_label)
            new_vmp_header["Map"][1]["LUTFileName"] = "eccentricity_v1.olt"

            # Norm t-value map
            new_vmp_header["Map"][2]["MapName"] = "Sensitivity Map (L2Norm)"
            new_vmp_header["Map"][2]["NrOfUsedVoxels"] = vox_norm.size
            new_vmp_header["Map"][2]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][2]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][2]["UpperThreshold"] = np.percentile(vox_norm, 95)
            new_vmp_header["Map"][2]["MapThreshold"] = np.percentile(vox_norm, 5)
            new_vmp_header["Map"][2]["LUTFileName"] = "faruk_curvature_colorbrewer.olt"

            # Divergenge map
            new_vmp_header["Map"][3]["MapName"] = "Specificity Map (1-Divergence)"
            new_vmp_header["Map"][3]["NrOfUsedVoxels"] = vox_div.size
            new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
            new_vmp_header["Map"][3]["ShowPosNegValues"] = 1
            new_vmp_header["Map"][3]["UpperThreshold"] = np.percentile(vox_div, 95)
            new_vmp_header["Map"][3]["MapThreshold"] = np.percentile(vox_div, 5)
            new_vmp_header["Map"][3]["LUTFileName"] = "faruk_curvature_colorbrewer.olt"

            # Export VMP
            basename = IN_FILE.split(os.extsep, 1)[0]
            OUTNAME = "{}{}_preference_metrics_unthreshold.vmp".format(basename, out_suffix)
            bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)

            # %% Tuning curves data structure
            tuning_dict = {"SubjID": su, "VMR": FILENAME_VMP,
                            "TValues": vox_tvalue, "Label": vox_label,
                            "Sensitivity": vox_norm, "Specificity": vox_div}

            np.save("{}{}_tuning_dict_unthreshold".format(basename, out_suffix),
                    tuning_dict, allow_pickle=True)

print("Done.")
