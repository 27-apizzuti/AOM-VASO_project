""" Crete 4D nifti: from convoluted to flattened coordinate
from thingsonthings.org LN2_MULTILATERATE blog post."""


import os
import numpy as np
import pyvista as pv
import nibabel as nb

# Scalar file (e.g. activtion map or anatomical image)
PATH_IN= "D:\\Pilot_Exp_VASO\\pilotAOM\\Results\\Animations\\sub-02\\data\\folded_to_flatten"

FILE1 = os.path.join(PATH_IN, 'sub-02_seg_rim_4_9_curvature_binned_ZOOM.nii.gz')
FILE2 = os.path.join(PATH_IN, 'sub-02_UV_coordinates_zoom.nii.gz')
FILE3 = os.path.join(PATH_IN, 'sub-02_seg_rim_4_9_metric_equivol_zoom.nii.gz')
MASK = os.path.join(PATH_IN, 'sub-02_perimeter_chunk_boundary_masked_c100_bin_ZOOM.nii.gz')
NR_STEPS = 25
OUTFILE = os.path.join(PATH_IN, 'step1_curv_binn_{}steps_depth21'.format(NR_STEPS))

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
nii1 = nb.load(FILE1)

mask = nb.load(MASK).get_fdata()
mask = mask == 1

data1 = nii1.get_fdata() * mask
data2 = nb.load(FILE2).get_fdata()
data3 = nb.load(FILE3).get_fdata()
data3 = data3 * mask

# Prepare coordinates
dims = data1.shape
coords_xyz = np.asarray(np.indices(dims))
coords_xyz = np.transpose(coords_xyz, [1, 2, 3, 0])

coords_uvd = np.zeros(data1.shape + (3,))
coords_uvd[..., 0:2] = data2
coords_uvd[..., 2] = data3

# -----------------------------------------------------------------------------
# Adjust UVD coordinate range to fit in the data image matrix
# -----------------------------------------------------------------------------
coords_uvd[..., 0] -= np.min(coords_uvd[..., 0])
coords_uvd[..., 0] /= np.max(coords_uvd[..., 0])
coords_uvd[..., 0] *= dims[0]
# coords_uvd[..., 0] += 0.5

coords_uvd[..., 1] -= np.min(coords_uvd[..., 1])
coords_uvd[..., 1] /= np.max(coords_uvd[..., 1])
coords_uvd[..., 1] *= dims[1]
# coords_uvd[..., 1] += 0.5

coords_uvd[..., 2] = coords_uvd[..., 2] * 21 + (dims[2] / 2.)

# -----------------------------------------------------------------------------
# Interpolate voxel particle tractories
# -----------------------------------------------------------------------------
flat_xyz = coords_xyz[mask]
flat_uvd = coords_uvd[mask]
nr_voxels = np.sum(mask)

traj = np.zeros((nr_voxels, NR_STEPS, 3))
for i in range(nr_voxels):
    traj[i, :, 0] = np.linspace(flat_xyz[i, 0], flat_uvd[i, 0], NR_STEPS)
    traj[i, :, 1] = np.linspace(flat_xyz[i, 1], flat_uvd[i, 1], NR_STEPS)
    traj[i, :, 2] = np.linspace(flat_xyz[i, 2], flat_uvd[i, 2], NR_STEPS)

# -----------------------------------------------------------------------------
# Transform volume data
# -----------------------------------------------------------------------------
new_data = np.zeros(dims + (NR_STEPS,))
count = np.copy(new_data)
for i in range(nr_voxels):
    idx0 = int(traj[i, 0, 0])
    idx1 = int(traj[i, 0, 1])
    idx2 = int(traj[i, 0, 2])

    for j in range(NR_STEPS):
        new_idx0 = int(traj[i, j, 0])
        new_idx1 = int(traj[i, j, 1])
        new_idx2 = int(traj[i, j, 2])
        # Move voxels like particles
        new_data[new_idx0, new_idx1, new_idx2, j] += data1[idx0, idx1, idx2]
        count[new_idx0, new_idx1, new_idx2, j] += 1

# Normalize summed values with counts to attain mean
new_data[count != 0] /= count[count != 0]

# Save as nifti
img = nb.Nifti1Image(new_data, affine=nii1.affine, header=nii1.header)
nb.save(img, OUTFILE)

print("Finished.")
