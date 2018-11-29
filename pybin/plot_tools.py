# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 11:36:30 2018

@author: cs17809
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_merge(idx, ims, ids, span):
    centre = len(ids) // 2 - 1 + span % 2
    print('\nWorking on {}'.format(ids[centre]))
    f_ax=-1
    # Prettify subplots (2 rows) if outputting > 6
    if len(ims) + 1 > 6:
        ncols = -(-(len(ims) + 1) // 2)
        nrows = 2
        f, (axes) = plt.subplots(nrows=nrows, ncols=ncols)
        axes=axes.flatten()
        if span % 2 == 0:
            axes[-1].axis('off')
            f_ax = -(2 - span % 2)
    else:
        f, (axes) = plt.subplots(nrows=1, ncols=len(ims) + 1)
    
    # Plot each of the images used to make the merged image
    for ax, im, im_id in zip(axes[:f_ax], ims, ids):
        ax.imshow(im, cmap='gray')
        ax.set_title(im_id)
            
    axes[f_ax].imshow(np.nanmean(ims, axis=0), cmap='gray')
    axes[f_ax].set_title('Merged', color='r')
    plt.setp(tuple(axes[f_ax].spines.values()), color='r')
    
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])     
    plt.show()