"""
Created on Fri Dec 10 12:26:43 2021

Exploration of compoda library

NB: Only positive values

@author: apizz
"""

import nibabel as nb
import numpy as np
import os
from compoda.core import closure, aitchison_norm, aitchison_dist, power

data_test = np.asarray([
    [4, 2, 2, 2],
    [2, 4, 2, 2],
    [2, 2, 4, 2],
    [2, 2, 2, 4],
    [4, 4, 2, 2],
    [4, 2, 3.8, 2],
    [4, 4, 4, 2]])

data_baric = closure(data_test, k=1.0)  # vector in simplex space with barycentric coordinates

anorm = aitchison_norm(data_baric)  # specificity

# Reference points in simplex space
ref_array = np.asarray([
    [0.7, 0.1, 0.1, 0.1],
    [0.1, 0.7, 0.1, 0.1],
    [0.1, 0.1, 0.7, 0.1],
    [0.1, 0.1, 0.1, 0.7],
    [0.4, 0.4, 0.1, 0.1],
    [0.1, 0.4, 0.4, 0.1],
    [0.1, 0.1, 0.4, 0.4],
    [0.4, 0.1, 0.4, 0.1],
    [0.1, 0.4, 0.1, 0.4],
    [0.4, 0.1, 0.1, 0.4],
    [0.3, 0.3, 0.3, 0.1],
    [0.1, 0.3, 0.3, 0.3],
    [0.3, 0.1, 0.3, 0.3],
    [0.3, 0.3, 0.1, 0.3]])

# Scaling: make ref points lying on a sphere
anorm_ref_array = aitchison_norm(ref_array)

scal_f = anorm_ref_array[0, None] / anorm_ref_array

scal_ref_array = power(ref_array, scal_f[..., None])

anorm_scal_check = aitchison_norm(scal_ref_array)  # CHECK OK

# Compute distances
dist_field = np.zeros((data_baric.shape[0], ref_array.shape[0]))

for it in range(scal_ref_array.shape[0]):
    temp = np.tile(scal_ref_array[it, :, None], data_baric.shape[0]).T
    dist_field[:, it] = aitchison_dist(data_baric, temp)

idx_min = np.argmin(dist_field, axis=1)


class_data = np.zeros(data_baric.shape[0])

idx_mono = np.in1d(idx_min, [0, 1, 2, 3])
idx_bi = np.in1d(idx_min, np.arange(4, 10))
idx_tri = np.in1d(idx_min, np.arange(10, 14))

class_data[idx_mono] = 1
class_data[idx_bi] = 2
class_data[idx_tri] = 3
