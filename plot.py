"""
Created on Tue Jun 20 12:22:45 2017

@author: Hyeonguk Park
"""
#%%
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np

a4 = np.zeros(20)

with open("../images/bendera4.dat") as BENDER:
    i=0
    for line in BENDER:
        a4[i] = line
        i += 1
        
def plot_result(ngc_num,n):
    
    with open("../results/%s.dat" % ngc_num) as f:
        i=0
        x = np.zeros(18)
        B4 = np.zeros(18)
        scale = np.zeros(18)
        for line in f:
            xt,yt,scalet=line.split()
            x[i]=float(xt)
            B4[i]=float(yt)*float(scalet)
            scale[i]=float(scalet)
            i += 1    
        f.close()
    
    plt.figure(figsize=(3,3))
    plt.scatter(x,B4,color='black')
    plt.xscale('log')
    plt.title("a4/a value for NGC %s" % ngc_num)
    plt.ylabel("a4/a")
    plt.xlabel('semimajor axis (arcsec)')
    if a4[n] < 10:
        aa = np.ones(np.shape(x))*a4[n]*0.01
        plt.plot(x,aa,color='red')
    plt.savefig('../results/%s.png' % ngc_num,bbox_inches='tight')
    plt.show()


with open("../images/names.list") as fname:
    i=0
    for line in fname:
        name = line[:-1]
        ngc_num = name[3:]
        
        plot_result(ngc_num,i)
        i += 1
    fname.close()