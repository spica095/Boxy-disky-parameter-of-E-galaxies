"""
Created on Mon Jun 19 00:07:09 2017

@author: Hyeonguk Park
"""

import numpy as np
from photutils import DAOStarFinder
from photutils import aperture_photometry as APPHOT
from photutils import CircularAperture as CircAp
from photutils import Background2D

def Starfind(img,FWHM):

    find   = DAOStarFinder(fwhm=FWHM, threshold=0.15, # I quite arbitrarily chose 0.5
                           sharplo=0.2, sharphi=1.0,  # default values
                           roundlo=-1.0, roundhi=1.0, # default values
                           sigma_radius=5,            # default=1.5
                           ratio=1.0,                 # 1.0: circular gaussian
                           exclude_border=True)       # To exclude sources near edges

    found = find(img)
    
    box  = (10, 10)
    filt = (5, 5)
    bkg = Background2D(img, box_size=box, filter_size=filt).background
    
    r = np.max((3, FWHM))
    coord = (found['xcentroid'], found['ycentroid'])
    apert = CircAp(coord, r=r)
    img_bs = img - bkg
    phot  = APPHOT(data=img_bs, apertures=apert)
    
    return phot
