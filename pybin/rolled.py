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

    
def revolve_replace(im_list, span, stop = 3, load=False, mirror=True):
    
    # Mirror start data [3, 2, 1, 1, 2, 3]
    start = span//2 - (span+1) % 2
    if mirror:
        stack = im_list[:start][::-1] + im_list[:span - start]
    # Or continue same value  [1, 1, 1, 1, 2, 3]
    else:
        stack = im_list[:1] * start + im_list[:span - start]
    
    # Load corresponding images if true
    if load:
        stack = [imageio.imread(im_id) for im_id in stack]
    
    # Iterate and yield values
    i = span-start
    while i < span - start + stop:
        yield stack
        new_stack = np.roll(stack, -1, axis=0)
        
        if i >= len(im_list) + start + 1 - span % 2:      
            return
            yield
        elif i >= len(im_list):
            im_id = im_list[len(im_list) - i - 1] if mirror else im_list[-1]
        else:
            im_id = im_list[i]
        
        if load:
            new_stack[-1] = imageio.imread(im_id)
        else:
            new_stack[-1] = im_id
        stack = new_stack
        i += 1
        
        

class Rolled:
    
    def __init__(self, im_folder, ext='tif', span=3, mirror=True, 
                 hdf_fpath=None, hdf_groups=None):
        
        self.iloc = os.path.realpath(im_folder)
        self.im_names = [im for im in sorted(os.listdir(self.iloc)) if im[-3:] == ext]
        self.im_paths = [os.path.join(self.iloc, i) for i in self.im_names]
        self.num_ims = len(self.im_names) # len(ims)
        self.dtype = imageio.imread(self.im_paths[0]).dtype
        self.span = span
        self.mirror = mirror
        self.hdf_fpath = hdf_fpath
        self.hdf_groups = hdf_groups
        
        assert span < self.num_ims, 'Span larger than number of images'
        print('{} images...'.format(self.num_ims))
        
        
    def stack_create(self, stop):
        stack = revolve_replace(self.im_paths, self.span, stop, True, self.mirror)
        stack_names = revolve_replace(self.im_names, self.span, stop, False, self.mirror)
        
        return stack, stack_names
    
    def name_test(self, stop=3):
        """
        Simple test to check  that the correct files are merged.
        """
        stack, stack_names = self.stack_create(stop)
        for idx, (ims, i) in enumerate(zip(stack, stack_names)):
            print(idx, i)
            
            
    def roll_test(self, stop=3):
        
        stack, stack_names = self.stack_create(stop)
        for idx, (ims, ids) in enumerate(zip(stack, stack_names)):
            plot_merge(idx, ims, ids, self.span)
            
            
    def roll_save(self, save_folder, data={}, hdf=True, overwrite=True):
        save_folder = os.path.abspath(save_folder)
        stack, stack_names = self.stack_create(stop=self.num_ims)
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        save_paths=[]        
        for idx, (ims, ids) in enumerate(zip(stack, stack_names)):
            centre = len(ids) // 2 - 1 + self.span % 2
            save_path = os.path.join(save_folder, ids[centre])
            save_paths.append(save_path)
            im_bin = np.nanmean(ims, axis=0).astype(self.dtype)
            print(save_path)
            imageio.imwrite(save_path, im_bin)
        
        if hdf:
            p0, p1 = os.path.split(os.path.abspath(save_folder))
            #print(p0, p1)
            ext = '.h5' if self.hdf_fpath is None else os.path.splitext(self.hdf_fpath)[-1]
            save_path = os.path.join(p0, '{}{}'.format(p1, ext))
            #print(save_path)
            hdf_create_mod(self.hdf_fpath, save_path, save_paths, 
                           self.hdf_groups, data, overwrite) 

                

        
if __name__ == "__main__":
    iloc = 'test_images/'#'N:/Work Data/ee18836-1/rawdata/77696/'#'W:/ee18836-1/rawdata/77696/'
    sloc = 'test_merge/'
    #iloc='W:/ee18836-1/rawdata/77695/'
    test = Rolled(iloc, span=3, mirror=True)
    test.roll_test()
    test.roll_save('processing/test/')
    
    test2 = Rolled('processing/test/', hdf_fpath='processing/test.h5', hdf_groups=['images'], span=5, mirror=True)
    test2.roll_test()
    test2.roll_save('processing/testle2/')
    #test.merge_test(2)
    #test.merge_save(sloc)
    
