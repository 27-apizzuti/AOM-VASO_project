"""
Created on Thu Oct 28 14:21:14 2021
Patch Flattening script: anatomical images
NB: This script computes automatically the number of bin that should be used (x,y,z) once decided the "nominal (desired) resolution for the flattened domain"
Remeber to check the density file!!!
@author: apizz
"""
import os
import numpy as np
import nibabel as nb
import subprocess
import math

STUDY_PATH = "/mnt/d/Pilot_Exp_VASO/pilotAOM"
SUBJ = ['sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']
RADIUS = [15, 13, 12, 13, 16]
CONDT = ['standard']
ROI_NAME = ['leftMT_Sphere16radius']
NOM_RES = 0.05   # original resolution 0.2 iso mm

for iterSbj, su in enumerate(SUBJ):
    PATH_FLAT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'flattening_4_r_{}_cp_0'.format(RADIUS[iterSbj]))
    PATH_LAY = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'layers_4')
    PATH_EPI = os.path.join(STUDY_PATH, su, 'derivatives', 'func', 'AOM', 'vaso_analysis', 'standard', 'masks_maps', 'res_pt2')

    OUTPUT_DIR = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'patch_flatten')
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # VALUES = [ os.path.join(STUDY_PATH, su, 'derivatives', 'anat', 'segmentation_4', '{}_acq-mp2rage_UNI_ss_warp_resl_slab_scaled_4.nii.gz'.format(su)),
    #             os.path.join(PATH_LAY, '{}_seg_rim_4_9_curvature_binned.nii'.format(su)),
    #             os.path.join(PATH_EPI, '{}_BOLD_mean_scaled_4.nii.gz'.format(su))]
    VALUES = [ os.path.join(PATH_LAY, '{}_seg_rim_4_9_thickness.nii'.format(su))]

    COORD_UV = os.path.join(PATH_FLAT, '{}_UV_coordinates.nii'.format(su))
    COORD_D = os.path.join(PATH_LAY,'{}_seg_rim_4_9_metric_equivol.nii'.format(su))
    DOMAIN = os.path.join(PATH_FLAT, '{}_perimeter_chunk_boundary_masked_c100_bin.nii.gz'.format(su))

    # 1) Find the cortical thickness of the disk
    NII_FILE1 = os.path.join(PATH_LAY, '{}_seg_rim_4_9_thickness.nii'.format(su))
    nii1 = nb.load(NII_FILE1)
    thick = nii1.get_fdata()

    NII_FILE2 = os.path.join(PATH_FLAT, '{}_perimeter_chunk.nii'.format(su))
    nii2 = nb.load(NII_FILE2)
    mask = nii2.get_fdata()
    chunk_thick = np.mean(thick[mask > 0])
    print('Average cortical thickness of the chunk: {}'.format(chunk_thick))
    binZ = 2 * math.ceil( chunk_thick / NOM_RES )
    if binZ % 2 == 0:
        binZ = binZ + 1

    # 2) Find binX, binY
    chunk_area = math.pi * (RADIUS[iterSbj]*RADIUS[iterSbj])
    binX = math.ceil( math.sqrt(chunk_area / (NOM_RES*NOM_RES)) )
    print('BinZ {}, BinX {}'.format(binZ, binX))

    for j, values in enumerate(VALUES):
        # Determine output basename
        filename = os.path.basename(values)
        basename, ext = filename.split(os.extsep, 1)
        outname = os.path.join(OUTPUT_DIR, "{}_binz_{}.{} ".format(basename, binZ, ext))
        print(outname)
        print('Flattening {}'.format(filename))

        command = "LN2_PATCH_FLATTEN "
        command += "-values {} ".format(values)
        command += "-coord_uv {} ".format(COORD_UV)
        command += "-coord_d {} ".format(COORD_D)
        command += "-domain {} ".format(DOMAIN)
        command += "-bins_u {} ".format(binX)
        command += "-bins_v {} ".format(binX)
        command += "-bins_d {} ".format(binZ)
        command += "-voronoi "
        command += "-density "
        command += "-output {} ".format(outname)
        subprocess.run(command, shell=True)
