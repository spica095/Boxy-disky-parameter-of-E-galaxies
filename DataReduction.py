"""
Created on Mon Jun 19 01:05:32 2017

@author: Hyeonguk Park
"""

from matplotlib import pyplot as plt
import numpy as np
import sliceGAL 
import Starfinder
import Isophote
import CoordTf
import fitB4 as fit

"""
The names of the images have form of ngc***r.fits
names.list contains names of object like ngc315, ngc3610, ...
"""

with open("../images/names.list") as fname:
    for line in fname:
        name = line[:-1] + 'r'                  #example : ngc315r
        imgname = '../images/%s.fits' % name    
        ngc_num = imgname[13:-6]                #example : 315
        
        print('CURRENT GALAXY : %s' % ngc_num)
        
        FWHM = 1.57
        
        img = sliceGAL.ImageSlice(imgname)      #cropping image
        
        phot_star = Starfinder.Starfind(img,FWHM)#star finding and aperture photometry
        
        cs = Isophote.ContourSet(img)           #drawing isophotes
        
        
        f = open('../results/%s.dat' % ngc_num,'w')
        n_iso = len(cs.collections)
        
        for i in range(1,n_iso):
            
            coord = Isophote.IsophoteCoord(cs,i,phot_star,FWHM)
            
            z = CoordTf.fitEllipse(coord[0],coord[1]) #ellipse fitting
            coord_iso = CoordTf.CT_to_Unit_Cir(coord,z) #coordinate transf.
            axes = CoordTf.ellipse_axis_length(z)       #lengths of semi-axes.
            axes.sort()             #axes[1] : semi-major axis
            axis = axes[1]*0.396    #pixel size of SDSS image in arcsec
            scale = np.sqrt(axes[0]/axes[1]) #normalization scale factor
                                                # to compare results with Bender's
            B4 = fit.fitB4(coord_iso)
            fdat = '%e %e %e\n' % (axis,B4,scale)
            f.write(fdat)
        
        f.close()
        