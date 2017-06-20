"""
Created on Mon Jun 19 01:05:32 2017

@author: Hyeonguk Park
"""
#%%
from matplotlib import pyplot as plt
import numpy as np
import sliceGAL 
import Starfinder
import Isophote
import CoordTf
import fitB4 as fit

with open("../images/names.list") as fname:
    for line in fname:
        name = line[:-1] + 'r'
        imgname = '../images/%s.fits' % name
        ngc_num = imgname[13:-6]
        
        FWHM = 1.57
        
        img = sliceGAL.ImageSlice(imgname)
        
        phot_star = Starfinder.Starfind(img,FWHM)
        
        cs = Isophote.ContourSet(img)
        
        
        f = open('../results/%s.dat' % ngc_num,'w')
        n_iso = len(cs.collections)
        
        for i in range(1,n_iso):
            
            coord = Isophote.IsophoteCoord(cs,i,phot_star,FWHM)
            
            z = CoordTf.fitEllipse(coord[0],coord[1])
            coord_iso = CoordTf.CT_to_Unit_Cir(coord,z)
            
            
            B4 = fit.fitB4(coord_iso)
            fdat = '%d %e\n' % (i,B4)
            f.write(fdat)
        
        f.close()