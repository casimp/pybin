# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:22:47 2018

@author: cs17809
"""
import numpy as np
import os
import h5py
from shutil import copy2


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

    
def create_hdf(spath, im_fpaths, data={}, hdf_path='image_data', overwrite=False):
    # All to be 'entry1/time' 'entry1/image_data' or 'time', 'image_data' 
    # Don't combine!
    f = h5py.File(spath, 'a' if overwrite else 'w-')
    
    im_fpaths = np.array([[i.replace('\\', '/').encode('utf-8')] for i in im_fpaths]).astype('|S255')
    try:
        del f[hdf_path]
        for key in data:
            del f[key]
    except:
        pass

    f.create_dataset(hdf_path, data=im_fpaths, maxshape=(None, 1), chunks=(1,1))
    for name, value in zip(['data_filename', 'signal', 'target'], 
                           [1, 1, hdf_path.encode('utf-8')]):
        f[hdf_path].attrs.create(name, value, shape=None, dtype=None)
    
    for key in data:
        f.create_dataset(key, data=data[key])
        f[key].attrs.create('target', key.encode('utf-8'), shape=None, dtype=None)
        
    f.close()

def hdf_create_mod(hdf_fpath, save_path, im_paths, hdf_groups=None, 
                   data={}, overwrite=True):
    
    if hdf_fpath is not None:
        #print(hdf_fpath, save_path)
        copy2(hdf_fpath, save_path)
        mod_paths(save_path, im_paths, hdf_groups)
        
    else:
        create_hdf(save_path, im_paths, data, 'images', overwrite=overwrite)    
