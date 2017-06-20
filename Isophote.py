"""
Created on Mon Jun 19 01:01:50 2017

@author: Hyeonguk Park
"""
#%%
from scipy.signal import medfilt
from matplotlib import pyplot as plt
import numpy as np

def ContourSet(img):
    med_img = medfilt(img,kernel_size=11)
    cs = plt.contour(med_img, np.arange(0.1,2,0.1), origin='lower')
    return cs

def IsophoteCoord(cs, n_iso, phot_star, FWHM):
    n = len(cs.collections[n_iso].get_paths())
    d = np.zeros(n)
    for j in range(0,n):
        d[j] = len(cs.collections[n_iso].get_paths()[j])
        n_gal = np.argmax(d)

    #To get the path list of the 10th contourline 
    p = cs.collections[n_iso].get_paths()[n_gal]
    v = p.vertices
    
    #The x and y coordinate of the contourline(isophote)
    x = v[:,0]
    y = v[:,1]
    
    sigma = FWHM / (2 * np.sqrt(2 * np.log(2)))
    
    for i in range(1,len(phot_star)):
        xs, ys = phot_star['xcenter'][i].value, phot_star['ycenter'][i].value
        flux = phot_star['aperture_sum'][i]
        if flux > 30: flux = 30.
        for j in range(len(x)-1,-1,-1):
            if np.sqrt((x[j]-xs)**2+(y[j]-ys)**2) < flux*sigma : 
                x = np.delete(x, (j), axis=0)
                y = np.delete(y ,(j), axis=0)

    coord = np.zeros((2,len(x)))
    coord[0] = x
    coord[1] = y
    
    return coord