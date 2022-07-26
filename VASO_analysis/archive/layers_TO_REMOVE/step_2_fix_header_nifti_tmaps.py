"""
Created on Thu Oct 14 14:57:29 2021
Fixing header for T-maps using ANATOMY FILE

Run WSL (python .py)

@author: apizz
"""

import os
import subprocess


STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']      # , 'rightMT_Sphere16radius'
MAPS_NAME = ['winner_map', 'sensitivity', 'specificity']

for roi in ROI_NAME:

    for i, su in enumerate(SUBJ):

        REF_NIFTI = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'alignment_ANTs', '{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI', 'exported_nifti')
        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'layers_columns')

        if not os.path.exists(PATH_OUT):
            print("Creating folders")
            os.mkdir(PATH_OUT)
            os.mkdir(os.path.join(PATH_OUT, 'res_pt8'))
            os.mkdir(os.path.join(PATH_OUT, 'res_pt8', 't_maps'))
            os.mkdir(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps'))


        # %% Single t-maps
        for itmap, name_map in enumerate(MAPS_NAME):

            in_B = "{}_{}_BOLD_{}_unthreshold.nii.gz".format(su, roi, name_map)
            in_V = "{}_{}_VASO_{}_unthreshold.nii.gz".format(su, roi, name_map)

            command = "fslmaths "
            command += "{} ".format(REF_NIFTI)
            command += "-mul 0 "
            command += "-add "
            command += "{} ".format(os.path.join(PATH_IN, in_B))
            command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_BOLD_{}_unthreshold_fix_hd.nii.gz".format(su, roi, name_map)))
            print("{}, {}, Fixing BOLD {} tmap".format(su, roi, name_map))
            subprocess.run(command, shell=True)

            command = "fslmaths "
            command += "{} ".format(REF_NIFTI)
            command += "-mul 0 "
            command += "-add "
            command += "{} ".format(os.path.join(PATH_IN, in_V))
            command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_VASO_{}_unthreshold_fix_hd.nii.gz".format(su, roi, name_map)))
            print("{}, {}, Fixing VASO {} tmap".format(su, roi, name_map))
            subprocess.run(command, shell=True)

        # #%% More input files
        # FILE_V = os.path.join(PATH_IN, "{}_{}_VASO_BOLDmask_t_map.nii.gz".format(su, roi))
        # FILE_B = os.path.join(PATH_IN, "{}_{}_BOLD_t_map.nii.gz".format(su, roi))

        # CV_FILE_V = os.path.join(PATH_IN, "{}_{}_CV_VASO_BOLDmask_t_map.nii.gz".format(su, roi))
        # CV_FILE_B = os.path.join(PATH_IN, "{}_{}_CV_BOLD_t_map.nii.gz".format(su, roi))

        # CV_WM_FILE_V = os.path.join(PATH_IN, "{}_{}_CV_VASO_BOLDmask_winner_map.nii.gz".format(su, roi))
        # CV_WM_FILE_B = os.path.join(PATH_IN, "{}_{}_CV_BOLD_winner_map.nii.gz".format(su, roi))

        # CV_SENS_FILE_V = os.path.join(PATH_IN, "{}_{}_CV_VASO_BOLDmask_sensitivity_map.nii.gz".format(su, roi))
        # CV_SENS_FILE_B = os.path.join(PATH_IN, "{}_{}_CV_BOLD_sensitivity_map.nii.gz".format(su, roi))

        # CV_SPEC_FILE_V = os.path.join(PATH_IN, "{}_{}_CV_VASO_BOLDmask_specificity_map.nii.gz".format(su, roi))
        # CV_SPEC_FILE_B = os.path.join(PATH_IN, "{}_{}_CV_BOLD_specificity_map.nii.gz".format(su, roi))
        # # %% AVG t-map
        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(FILE_B)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 't_maps', "{}_{}_BOLD_t_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing AVG-BOLD tmap".format(su, roi))
        # subprocess.run(command, shell=True)

        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(FILE_V)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 't_maps', "{}_{}_VASO_BOLDmask_t_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing AVG-VASO tmap".format(su, roi))
        # subprocess.run(command, shell=True)

        # # %% CV-AVG t-map
        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_FILE_B)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 't_maps', "{}_{}_CV_BOLD_t_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-BOLD tmap".format(su, roi))
        # subprocess.run(command, shell=True)

        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_FILE_V)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 't_maps', "{}_{}_CV_VASO_BOLDmask_t_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-VASO tmap".format(su, roi))
        # subprocess.run(command, shell=True)

        # # %% CV-AVG winner maps
        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_WM_FILE_B)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_BOLD_winner_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-BOLD winner map".format(su, roi))
        # subprocess.run(command, shell=True)

        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_WM_FILE_V)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_VASO_BOLDmask_winner_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-VASO winner map".format(su, roi))
        # subprocess.run(command, shell=True)

        # # %% CV-AVG specificity maps
        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_SPEC_FILE_B)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_BOLD_specificity_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-BOLD specificity map".format(su, roi))
        # subprocess.run(command, shell=True)

        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_SPEC_FILE_V)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_VASO_BOLDmask_specificity_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-VASO specificity map".format(su, roi))
        # subprocess.run(command, shell=True)

        # # %% CV-AVG sensitivity maps
        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_SENS_FILE_B)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_BOLD_sensitivity_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-BOLD sensitivity map".format(su, roi))
        # subprocess.run(command, shell=True)

        # command = "fslmaths "
        # command += "{} ".format(REF_NIFTI)
        # command += "-mul 0 "
        # command += "-add "
        # command += "{} ".format(CV_SENS_FILE_V)
        # command += "{}".format(os.path.join(PATH_OUT, 'res_pt8', 'winner_maps', "{}_{}_CV_VASO_BOLDmask_sensitivity_map_fix_hd.nii.gz".format(su, roi)))
        # print("{}, {}, Fixing CV AVG-VASO sensitivity map".format(su, roi))
        # subprocess.run(command, shell=True)

    print("Done.")
