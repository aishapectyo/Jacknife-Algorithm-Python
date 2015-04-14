#!/usr/bin/env python

# Estimate parameters/errors using jacknife
# by A. Mahmoud-Perez

import sys
import os
import numpy as np
from pylab import *
import scipy
import scipy.spatial
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import random
from array import *
import numpy
from random import randrange, uniform


data=np.genfromtxt('data.txt')
x=data[:,0]
y=data[:,1]

#apply a linear fit
def fit_func(x,a,b):
	return a*x +b

params = curve_fit(fit_func, x, y)
[a,b]=params[0]
print('slope and intercept for unrandomized data: ',a,b)

#plot for unrandomized data with its line of best fit.
#plt.figure(1)
#plt.plot(x,y,marker='.', linestyle=' ',color='m',)
#plt.plot(x, a*x+b)

slope_all=[]
inter_all=[]

#Get random samples with slopes and intercepts(used least squares approx.)
for j in range(100):
	for i in range(14):
		t = random.sample(data, 15)
		n = np.array(t)
		x=n[:,0]
		y=n[:,1]
		if i == 0:
			new_x=np.delete(x,0)
			new_y=np.delete(y,0)
		else:
			new_x=np.delete(x,i)
			new_y=np.delete(y,i)
	
		preavgx = sum(new_x)
		avgx = preavgx/15
		preavgy = sum(new_y)
		avgy = preavgy/15
		nom = new_y*(new_x - avgx)
		den = (new_x**2-avgx**2)
		top_sum = sum(nom)
		bot_sum = sum(den)
		slope = top_sum/bot_sum
		intercept = avgy - slope*avgx
	slope_all.append(slope)
	inter_all.append(intercept)


res_slope = 0
mtot = 0
for i in range(1,100):
        l= (slope_all[i]-2.210)**2
	res_slope = res_slope + l
	mtot = mtot + slope_all[i]
res=res_slope*0.01
sig = sqrt(res)
avgm = mtot/100
print('average slope: ', avgm)
print('error in slope with an N = 100: ', sig)


res_intercept = 0
itot = 0
for i in range(1,100):
	h = ((inter_all[i]-28.84)**2)/100.
	res_intercept = res_intercept + h
	itot =  itot + inter_all[i]
resi = res_intercept*0.01
sigti = sqrt(resi)
avgi=itot/100
print('average intercept: ', avgi)
print('error in intercept with an N = 100: ', sigti)
