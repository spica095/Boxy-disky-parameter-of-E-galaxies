"""
Created on Tue Jun 20 00:05:34 2017

@author: Hyeonguk Park
"""
    
from astropy.stats import sigma_clip
from astropy.modeling import models, fitting
import scipy.stats as stats
from matplotlib import pyplot as plt
import numpy as np

def fitB4(coord_iso):
    u = coord_iso[0]
    v = coord_iso[1]

    r = np.sqrt(u**2 + v**2)
    
    E=np.zeros(len(u))
    
    for i in range(0,len(u)):
        if np.sign(u[i])>0 and np.sign(v[i])>0 : E[i]=np.arctan(v[i]/u[i])
        elif np.sign(u[i])>0 and np.sign(v[i])<0 : E[i]=2*np.pi+np.arctan(v[i]/u[i])
        else : E[i]=np.pi+np.arctan(v[i]/u[i])
        
    Es = np.linspace(0,2*np.pi,num=100)



    dic = {'frequency': True, 'phase': True}
    
    g_init = (models.Sine1D(amplitude=0.1, frequency=1.5/np.pi, fixed=dic)
                +models.Sine1D(amplitude=0.1, frequency=2/np.pi, fixed=dic)
                +models.Sine1D(amplitude=0.1, frequency=1.5/np.pi,
                               phase=0.25, fixed=dic)
                +models.Sine1D(amplitude=0.1, frequency=2/np.pi,
                               phase=0.25, fixed=dic)
                +models.Const1D(amplitude=1.0,fixed={'amplitude':True}))
            
    fit = fitting.LevMarLSQFitter()
    or_fit = fitting.FittingWithOutlierRemoval(fit, sigma_clip, niter=3, sigma=3.0)
            
    filtered_data, or_fitted_model = or_fit(g_init, E, r)
    fitted_model = fit(g_init, E, r)
    
    plt.figure(figsize=(8,5))
    plt.plot(E, r, 'gx', label="original data")
    plt.plot(E, filtered_data, 'r+', label="filtered data")
    plt.plot(Es, fitted_model(Es), 'g-',
             label="model fitted w/ original data")
    plt.plot(Es, or_fitted_model(Es), 'r--',
             label="model fitted w/ filtered data")
    plt.legend(loc=2, numpoints=1)
    
    return or_fitted_model[3].amplitude.value