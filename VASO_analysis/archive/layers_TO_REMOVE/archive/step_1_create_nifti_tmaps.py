"""
Created on Thu Oct 14 12:26:05 2021

Create nifti files:

    AVG T-MAPS, Winner Map,
    CV-Winner Maps, CV Sensitivity Map, CV Specificity Map

    Unthresholded T-Maps:
        'horizontal', 'vertical', 'diag45', 'diag135'

@author: apizz
"""

import os
import numpy as np
import bvbabel
import nibabel as nb


STUDY_PATH = "D:\\Pilot_Exp_VASO\\pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']      # , 'rightMT_Sphere16radius'
MAPS_NAME = ['winner_map', 'sensitivity', 'specificity']

# T-value maps for layer profile
for roi in ROI_NAME:

    for i, su in enumerate(SUBJ):

        # Before Cross-validation (AVG results)

        REF_NIFTI = os.path.join('{}_acq-mp2rage_UNI_ss_warp_resl_slab.nii'.format(su))

        PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI')
        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
                               'vaso_analysis', CONDT[0], 'GLM', 'ROI', 'exported_nifti')

        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)
        FILE_V = "{}_VASO_interp_LN_meanRuns_standard_ROI_{}_c_thr_0_preference_metrics_unthreshold.vmp".format(su, roi)
        FILE_B = "{}_BOLD_interp_meanRuns_standard_ROI_{}_c_thr_0_preference_metrics_unthreshold.vmp".format(su, roi)

        header_B, data_B = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_B))
        header_V, data_V = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_V))

        for itmap, name_map in enumerate(MAPS_NAME):
            print('{}, {} Map ({})'.format(su, name_map, itmap))

            # Export UNTHRESHOLDED T-MAPS nifti
            outname_bold = os.path.join(PATH_OUT, "{}_{}_BOLD_{}_unthreshold.nii.gz".format(su, roi, name_map))
            img = nb.Nifti1Image(data_B[..., itmap+1], affine=np.eye(4))
            nb.save(img, outname_bold)

            outname_vaso = os.path.join(PATH_OUT, "{}_{}_VASO_{}_unthreshold.nii.gz".format(su, roi, name_map))
            img = nb.Nifti1Image((data_V[..., itmap+1]), affine=np.eye(4))
            nb.save(img, outname_vaso)



        # B_flat = data_B[..., 6].flatten()       # BOLD flattening: FDR + connected cluster map "All Cond vs Flick"
        # V_flat = data_V[..., 4].flatten() *-1

        # # Extract BOLDmask
        # idx = B_flat > 0
        # print("{}, {}, AVG: {}".format(su, roi, np.sum(idx)))

        # # Extract AVG t-map
        # bold_tmap = np.zeros(np.shape(B_flat))
        # vaso_tmap = np.zeros(np.shape(B_flat))

        # bold_tmap[idx] = B_flat[idx]
        # vaso_tmap[idx] = V_flat[idx]

        # bold_tmap = np.reshape(bold_tmap, [162, 216, 26])
        # vaso_tmap = np.reshape(vaso_tmap, [162, 216, 26])

        # # Export nifti
        # outname_bold = os.path.join(PATH_OUT, "{}_{}_BOLD_t_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(bold_tmap, affine=np.eye(4))
        # nb.save(img, outname_bold)

        # outname_vaso = os.path.join(PATH_OUT, "{}_{}_VASO_BOLDmask_t_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(vaso_tmap, affine=np.eye(4))
        # nb.save(img, outname_vaso)

        # # AVG winner map
        # FILE_WM_V = "{}_VASO_interp_LN_meanRuns_standard_ROI_{}_preference_metrics.vmp".format(su, roi)
        # FILE_WM_B = "{}_BOLD_interp_meanRuns_standard_ROI_{}_c_thr_4_preference_metrics.vmp".format(su, roi)

        # header_WM_B, data_WM_B = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_WM_B))
        # header_WM_V, data_WM_V = bvbabel.vmp.read_vmp(os.path.join(PATH_IN, FILE_WM_V))

        # # Export nifti
        # outname_bold = os.path.join(PATH_OUT, "{}_{}_BOLD_avg_winner_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(data_WM_B[..., 1], affine=np.eye(4))
        # nb.save(img, outname_bold)

        # outname_vaso = os.path.join(PATH_OUT, "{}_{}_VASO_avg_winner_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(data_WM_V[..., 1], affine=np.eye(4))
        # nb.save(img, outname_vaso)

        # #%% Cross validation
        # PATH_CV = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM',
        #                         'vaso_analysis', CONDT[0], 'cross_validation', 'Results')

        # CV_V = '{}_VASO_interp_LN_avg_cv_vox_{}_c_thr_4_BOLDMASK_c_thr_4.vmp'.format(su, roi)
        # CV_B = '{}_BOLD_interp_avg_cv_vox_{}_c_thr_4_c_thr_4.vmp'.format(su, roi)

        # header_B, CV_data_B = bvbabel.vmp.read_vmp(os.path.join(PATH_CV, CV_B))
        # header_V, CV_data_V = bvbabel.vmp.read_vmp(os.path.join(PATH_CV, CV_V))

        # # --------------- Winner Map
        # CV_B_flat = CV_data_B[..., 4].flatten()
        # CV_V_flat = CV_data_V[..., 4].flatten()
        # # --------------- T Map
        # cv_bold_tmap = np.zeros(np.shape(CV_B_flat))
        # cv_vaso_tmap = np.zeros(np.shape(CV_V_flat))

        # idx_B = CV_B_flat > 0
        # cv_bold_tmap[idx_B] = B_flat[idx_B]

        # idx_V = CV_V_flat > 0
        # cv_vaso_tmap[idx_V] = V_flat[idx_V]
        # print("{}, {}, CV-BOLD: {}".format(su, roi, np.sum(idx_B)))
        # print("{}, {}, CV-VASO: {}".format(su, roi, np.sum(idx_V)))

        # cv_bold_tmap = np.reshape(cv_bold_tmap, [162, 216, 26])
        # cv_vaso_tmap = np.reshape(cv_vaso_tmap, [162, 216, 26])

        # # Export nifti
        # outname_bold = os.path.join(PATH_OUT, "{}_{}_CV_BOLD_t_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(cv_bold_tmap, affine=np.eye(4))
        # nb.save(img, outname_bold)

        # outname_vaso = os.path.join(PATH_OUT, "{}_{}_CV_VASO_BOLDmask_t_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(cv_vaso_tmap, affine=np.eye(4))
        # nb.save(img, outname_vaso)

        # outname_wm_bold = os.path.join(PATH_OUT, "{}_{}_CV_BOLD_winner_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_B[..., 4], affine=np.eye(4))
        # nb.save(img, outname_wm_bold)

        # outname_wm_vaso = os.path.join(PATH_OUT, "{}_{}_CV_VASO_BOLDmask_winner_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_V[..., 4], affine=np.eye(4))
        # nb.save(img, outname_wm_vaso)

        # # ---------------- Specificity
        # outname_wm_bold = os.path.join(PATH_OUT, "{}_{}_CV_BOLD_specificity_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_B[..., 3], affine=np.eye(4))
        # nb.save(img, outname_wm_bold)

        # outname_wm_vaso = os.path.join(PATH_OUT, "{}_{}_CV_VASO_BOLDmask_specificity_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_V[..., 3], affine=np.eye(4))
        # nb.save(img, outname_wm_vaso)

        # # --------------- Sensitivity
        # outname_wm_bold = os.path.join(PATH_OUT, "{}_{}_CV_BOLD_sensitivity_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_B[..., 2], affine=np.eye(4))
        # nb.save(img, outname_wm_bold)

        # outname_wm_vaso = os.path.join(PATH_OUT, "{}_{}_CV_VASO_BOLDmask_sensitivity_map.nii.gz".format(su, roi))
        # img = nb.Nifti1Image(CV_data_V[..., 2], affine=np.eye(4))
        # nb.save(img, outname_wm_vaso)


    print("Finished.")
