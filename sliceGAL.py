
"""
Created on Sun Jun 18 21:40:47 2017

@author: Hyeonguk Park
"""

from astropy.io import fits
import numpy as np
from astropy.convolution import Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma
from photutils import detect_sources
from photutils import detect_threshold

"""
This ImageSlice function receives a filename string of the fits image.
Then this function opens fits file of given filename on current directory
or one may specify the directory name that the images are inside.
"""

def ImageSlice(imgname):

    hdu = fits.open(imgname)
    img = hdu[0].data

    threshold = detect_threshold(img, snr=4.)
    
    #Detection for every sources to find the position of the galaxy.
    sigma = 2. * gaussian_fwhm_to_sigma    # FWHM = 2.
    kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    kernel.normalize()
    segm = detect_sources(img, threshold, npixels=5, filter_kernel=kernel)

    segm_areas = segm.areas
    segm_areas = np.delete(segm.areas,0)    # deleting background area.
    label_gal = segm_areas.argmax()         # finding the galaxy by searching
                                            # a source which has largest area. 
    rslice = segm.slices[label_gal][0]      # row slice
    cslice = segm.slices[label_gal][1]      # column slice
    
    ri = rslice.start
    rf = rslice.stop
    ci = cslice.start
    cf = cslice.stop

    b = 0    # expanding constant   
    
    s_img = hdu[0].data[ri-b:rf+b,ci-b:cf+b]

    return s_img

