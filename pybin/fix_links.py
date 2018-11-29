# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 18:20:42 2018

@author: cs17809
"""
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import h5py

def mod_paths(fpath, im_paths, hdf_paths=None):
    # Used to simple modify the image path in the hdf5 files
    if hdf_paths is None:
        hdf_paths = ['entry1/pixium10_tif/image_data',
                    'entry1/instrument/pixium10_tif/image_data']
    
    f = h5py.File(fpath, 'r+')
    
    files = im_paths
    files = np.reshape(np.array(files, dtype='|S255'), (np.size(files), 1))
    for path in hdf_paths:
        for idx, i in enumerate(files):
            f[path][idx] = i
    print('Success (I think)')
    f.close()
    

base_folder = 'X:/ee18836-1/rawdata/'
runs = [77797, 77798, 77799,77800, 77801, 77802]
#77795, 77796, 
    
#base_folder = 'W:/ee18836-1/processing/S1/'

#merge = ['roll_2', 'roll_3']
#folders = [os.path.join(base_folder, m) for m in merge]

#for folder in folders:
#fpaths = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f[:-4] in files])


for run in runs:
    print(run)
    fpath = os.path.join(base_folder, '{}.nxs'.format(run))
    im_folder = os.path.join(base_folder, '{}/'.format(run))
    im_paths = sorted([os.path.join(im_folder, f) for f in os.listdir(im_folder)])
    
    mod_paths(fpath, im_paths, hdf_paths=None)
    

