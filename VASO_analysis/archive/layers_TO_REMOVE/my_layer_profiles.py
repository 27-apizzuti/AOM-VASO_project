"""
Created on Thu Oct 21 11:04:27 2021

@author: apizz
"""
import numpy as np

def my_layer_profiles(metric, n_lay):

    metric = metric.flatten()
    # layer quantization
    layers = np.ceil(metric * n_lay)
    return layers
