# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:44:20 2018

@author: cs17809
"""
import os
from rolled import Rolled
rawdata = 'W:/ee18836-1/rawdata'
processing = 'W:/ee18836-1/processing/S1/'

start = 77698
stop = 77715 + 1

for i in range(start, stop):
    images = os.path.join(rawdata, '{}'.format(i))
    hdf = os.path.join(rawdata, '{}.nxs'.format(i))
    
    for span in [2, 3]:
        data = Rolled(images, hdf_fpath=hdf, hdf_groups=None, span=span, mirror=True)
        #data.roll_test()
        data.roll_save(os.path.join(processing, 'roll_{}/{}'.format(span, i)))
    


