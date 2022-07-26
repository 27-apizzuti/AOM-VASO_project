"""
Created on Tue Dec  7 18:00:19 2021

Testing angular map

@author: apizz
"""

import numpy as np

TEMPL = np.array([[1, 0, -1, 0], [0, 1, 0, -1]])

t = np.asarray([1.1, 1, 0.8, 0.7])

t_templ = np.multiply(t, TEMPL)           # for each vox multiply t-value with the first coordinate dims: (2x4)
t_sum = np.sum(t_templ, axis=1)

# magnitude
normalized_t = t_sum / np.linalg.norm(t_sum, axis=0)

# inner_prod = np.inner(normalized_t, REF)

angle = np.arctan2(normalized_t[1], normalized_t[0])                # -> radians
# ----------------------------------
# Testing angle between two vector computation
T = np.array([[1, 0], [0, -1]])
magn =  np.linalg.norm(T, axis=1)
normalized_t = T / magn

angle = np.arctan2(normalized_t[1], normalized_t[0])                # -> radians
angle_degree = angle * 180 / np.pi       #range [-pi, pi]

if angle_degree < 0:
    angle_degree = 360 - np.abs(angle_degree)

final_angle_degree = angle_degree/2

print("For {} predicted angle is: {}".format(t, final_angle_degree) )

# Test different function
u = np.array([0, 0, 1])
v = np.array([1, 1, 1])
c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) # -> cosine of the angle
angle = np.arccos(np.clip(c, -1, 1))                # -> radiants
angle_degree = angle * 180 / np.pi
