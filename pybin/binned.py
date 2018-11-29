# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 19:05:46 2018

@author: cs17809
"""

import numpy as np
import os
import imageio

from hdf5_tools import hdf_create_mod  
from plot_tools import plot_merge       

               
            
class Binned:
    
    def __init__(self, im_folder, ext='tif', span=3, drop_end=True,
                 hdf_fpath=None, hdf_groups=None):
        self.iloc = os.path.realpath(im_folder)
        self.drop_end = drop_end
        self.span = span
        im_names = [i for i in sorted(os.listdir(self.iloc)) if i[-3:] == ext]
        print('\nFolder contains {} images.'.format(len(im_names)))
        rem = len(im_names) % self.span
        
        if rem > 0:
            im_names = im_names[:-rem] if self.drop_end else im_names[rem:]
            print('{} images cut to allow for binning.'.format(rem))
        
        self.im_names = im_names
        self.name_bins= np.reshape(self.im_names, (-1, self.span))
        
        self.im_paths = [os.path.join(self.iloc, i) for i in self.im_names]
        self.path_bins= np.reshape(self.im_paths, (-1, self.span))
        
        self.num_ims = len(self.im_names)
        self.dtype = imageio.imread(self.im_paths[0]).dtype
        self.hdf_fpath = hdf_fpath
        self.hdf_groups = hdf_groups
    
        assert span < self.num_ims, 'Span larger than number of images'
        
        print('Binned data to contain {} images.\n'.format(self.path_bins.shape[0]))
        
    def name_test(self, stop=3):
        
        stack, stack_names = self.stack_create(stop)
        for idx, (ims, i) in enumerate(zip(stack, stack_names)):
            print(idx, i)
            
    def bin_test(self, stop=3):
        
        stack, stack_names = self.path_bins, self.name_bins
        for idx, (ims, ids) in enumerate(zip(stack[:stop], stack_names[:stop])):

            ims = [imageio.imread(im) for im in ims]
            plot_merge(idx, ims, ids, self.span)
            
    def bin_save(self, save_folder, data={}, hdf=True, overwrite=True):
        save_folder = os.path.abspath(save_folder)
        stack, stack_names = self.path_bins, self.name_bins
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        save_paths=[]
        for idx, (ims, ids) in enumerate(zip(stack, stack_names)):
            ims = [imageio.imread(im) for im in ims]
            centre = len(ids) // 2 - 1 + self.span % 2
            save_path = os.path.join(save_folder, ids[centre])
            save_paths.append(save_path)
            
            im_bin = np.nanmean(ims, axis=0).astype(self.dtype)
            print(save_path)
            imageio.imwrite(save_path, im_bin)
        
        if hdf:
            p0, p1 = os.path.split(os.path.abspath(save_folder))
            ext = 'h5' if self.hdf_fpath is None else os.path.splitext(self.hdf_fpath)[-1]
            save_path = os.path.join(p0, '{}{}'.format(p1, ext))
            hdf_create_mod(self.hdf_fpath, save_path, save_paths, 
                           self.hdf_groups, data, overwrite)
          
            

        
if __name__ == "__main__":
    iloc = 'test_images/'
    sloc = 'test_merge/'

    test = Binned(iloc, span=2, drop_end=True)
    test.bin_test()
    test.bin_save('processing/bin_test/')
    
    test2 = Binned('processing/bin_test/', hdf_fpath='processing/test.h5', hdf_groups=['images'], span=2)
    test2.bin_test()
    test2.bin_save('processing/bin_test2/')

    
