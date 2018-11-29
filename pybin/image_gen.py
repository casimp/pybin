# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:45:18 2018

@author: cs17809
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import os
import sys
import imageio



for i in range(11):
    im = np.zeros((128, 128))
    np.random.seed(i)
    num_pixels = np.random.randint(1, 8)
    x, y = (123*np.random.random((2, num_pixels))).astype(np.int)
    im[x, y] = np.random.randint(1, 2**8 - 1, size=(num_pixels))
    
    
    gx, gy = np.random.randint(1, 30), np.random.randint(1, 30)
    bigger_points = ndimage.grey_dilation(im, structure=np.ones((gx, gy)), size=np.ones((gx, gy))).astype('uint8')
    
    square = np.zeros((16, 16))
    square[4:-4, 4:-4] = 1
    dist = ndimage.distance_transform_bf(square)
    dilate_dist = ndimage.grey_dilation(dist, size=(3, 3), \
            structure=np.ones((3, 3)))
    plt.figure()
    plt.imshow(np.invert(bigger_points), cmap='gray')
    imageio.imwrite('test_images/{:05d}.tif'.fodrmat(i), np.invert(bigger_points).astype('uint8'))