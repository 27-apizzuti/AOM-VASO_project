"""
Created on Thu Oct 28 14:21:14 2021
Evaluating "disk" coverage: how many activated voxels fit into the disk / total number of initial voxels
Activity volume computation.
Percentage of activity volume covered by the disk
NOTE: Quality check
@author: apizz
"""

import os
import numpy as np
import nibabel as nb
import subprocess

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
CONDT = ['standard']
FUNC = ["BOLD_CV_AVG", "VASO_CV_AVG"]
ROI_NAME = ['leftMT_Sphere16radius']
RADIUS = [15, 13, 12, 13, 16]
cp = 0
vox_vol = 0.2 * 0.2 * 0.2                    # mm3

# Execute
for iterSbj, su in enumerate(SUBJ):
    # 1) Create a binary mask of perimeter_chunk
    PATH_FLA = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_{}'.format(RADIUS[iterSbj], cp))
    PER_FILE = os.path.join(PATH_FLA, '{}_perimeter_chunk.nii'.format(su))
    MAS_FILE = os.path.join(PATH_FLA, '{}_perimeter_chunk_mask.nii'.format(su))
    CURV_FILE = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4', "{}_seg_rim_4_9_curvature.nii".format(su))

    print("For {}, Creating gray matter mask".format(su))
    command = "fslmaths "
    command += "{} ".format(PER_FILE)
    command += "-bin "
    command += "{}".format(MAS_FILE)
    subprocess.run(command, shell=True)

    for iterMask, mask in enumerate(FUNC):

        # 2) Load nifti and count initial n. of voxels (activity) and apply segmentation
        PATH_MASK = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', CONDT[0], 'masks_maps', 'res_pt2', 'masks')
        NII_FILE = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4.nii.gz'.format(su, ROI_NAME[0], mask))
        nii1 = nb.load(NII_FILE)
        vox_mask = nii1.get_fdata()
        idx1 = vox_mask > 0

        # Load curvature file
        nii = nb.load(CURV_FILE)
        curv = nii.get_fdata()
        idx2 = (curv > 0) + (curv < 0)
        idx = idx1 * idx2  # into gray matter

        # Activation volume in gray matter
        nvox = np.sum(idx)
        vol = nvox*vox_vol
        print("For {}, {}, activation volume: {:.3f} cm3".format(su, mask, vol/1000))

        # Percentage of activation with respect to curvature
        curv_roi = curv[idx > 0]
        step = (np.max(curv_roi)-np.min(curv_roi))/3
        sul = np.sum(curv_roi < np.min(curv_roi) + step)
        wall = np.sum((curv_roi > np.min(curv_roi) + step) * (curv_roi < np.max(curv_roi) - step))
        gyr = np.sum((curv_roi > np.max(curv_roi) - step) * (curv_roi < np.max(curv_roi)))
        print("{} activation vs curvature [s:{:.1f}%, w:{:.1f}%, g:{:.1f}%]".format(su, (sul*vox_vol/vol)*100, (wall*vox_vol/vol)*100, (gyr*vox_vol/vol)*100))

        # 3) Apply perimeter chunck
        OUTPUTNAME = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4_gray_matter_disk_r_{}_cp_{}.nii.gz'.format(su, ROI_NAME[0], mask, RADIUS[iterSbj], cp))
        command = "fslmaths "
        command += "{} ".format(NII_FILE)
        command += "-mas "
        command += "{} ".format(MAS_FILE)
        command += "{} ".format(OUTPUTNAME)
        subprocess.run(command, shell=True)

        # 4) Count voxels inside
        NII_FILE2 = os.path.join(PATH_MASK, '{}_{}_{}_mask_scaled_4_gray_matter_disk_r_{}_cp_{}.nii.gz'.format(su, ROI_NAME[0], mask, RADIUS[iterSbj], cp))
        nii2 = nb.load(NII_FILE2)
        vox_mask2 = nii2.get_fdata()
        nvox2 = np.sum(vox_mask2 > 0)
        print("For {}, {}, disk coverage: {:.1f}%".format(su, mask, (nvox2/nvox)*100))
