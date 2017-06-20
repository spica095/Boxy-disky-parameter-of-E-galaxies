"""
Created on Tue Jun 20 12:22:45 2017

@author: Hyeonguk Park
"""
#%%
from matplotlib import pyplot as plt
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
        for line in f:
            xt,yt=line.split()
            x[i]=float(xt)
            B4[i]=yt
            i += 1    
        f.close()
    
    plt.figure(figsize=(3,3))
    plt.scatter(x,B4,color='black')
    plt.title("B4 value for NGC %s" % ngc_num)
    plt.ylabel("B4")
    plt.xlabel('semimajor axis (arcsec)')
    if a4[n] < 10:
        aa = np.ones(np.shape(x))*a4[n]
        plt.plot(x,aa,color='red')
    plt.savefig('../results/%s.png' % ngc_num)
    plt.show()


with open("../images/names.list") as fname:
    i=0
    for line in fname:
        name = line[:-1]
        ngc_num = name[3:]
        
        plot_result(ngc_num,i)
        i += 1
    fname.close()