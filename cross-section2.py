# -*- coding: utf-8 -*-
"""
Created on Thu Feb 04 17:08:51 2016

@author: yiyuezhuo
"""

import statsmodels.api as sm
import statsmodels.formula.api as smf
from select2 import parse
import numpy as np
import pandas as pd

def sample(path="SPA1901_09_28.v2"):
    return parse(path)
    
rd=sample()

def take(pop):
    dic={}
    for key in ['money','size','literacy']:
        dic[key]=float(pop[key])
    for key in ['nation','religion','type']:
        dic[key]=pop[key]
    dic['amoney']=dic['money']/dic['size']
    return dic

dt=pd.DataFrame([take(value) for value in rd['pop'].values()])
mod=smf.ols('amoney ~ type:religion+type:literacy+religion*literacy',data=dt)
#print mod.fit().summary()
res=mod.fit()
print res.summary()