# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 21:59:48 2016

@author: yiyuezhuo
"""

from select2 import parse
import numpy as np
import statsmodels.api as sm
import pandas as pd

type_l=['farmers', 'bureaucrats', 'capitalists', 'artisans', 'aristocrats', 'officers', 'clergymen', 'labourers', 'slaves', 'clerks', 'soldiers', 'craftsmen']
religion_l=['shiite', 'catholic', 'mahayana', 'theravada', 'animist', 'orthodox', 'jewish', 'hindu', 'protestant', 'gelugpa', 'shinto', 'coptic', 'sunni', 'sikh']
del type_l[8]
del religion_l[0]#解决虚拟变量陷阱
dummy_l=type_l+religion_l#虚拟变量
number_l=['money','size','literacy']#数值变量
map_l=['a_money']#之后计算变量
var_l=number_l+dummy_l+map_l#总变量列表
id_map={var_l[i]:i for i in range(len(var_l))}

#rd=parse('SPA1901_09_28.v2')

def get_mat2(rd):
    mat=[]
    for pop in rd['pop'].values():
        record=[]
        for nv in number_l:
            record.append(float(pop[nv]))
        for _type in type_l:
            record.append(1 if _type==pop['type'] else 0)
        for _religion in religion_l:
            record.append(1 if _religion==pop['religion'] else 0)
        for _map in map_l:
            if _map=='a_money':
                record.append(float(pop['money'])/float(pop['size']))
        mat.append(record)
    print 'mat shape',len(mat),'*',len(mat[0])
    T=zip(*mat)
    print 'mat',len(mat),'T',len(T)
    X=pd.DataFrame({var_l[i]:T[i] for i in range(len(T))})
    return X
    
def take_pop(rd,pop):
    pop_d={}
    for _type in type_l:
        pop_d[_type]=1.0 if pop['type']==_type else 0.0
    for _religion in religion_l:
        pop_d[_religion]=1.0 if pop['religion']==_religion else 0.0
    for _number in number_l:
        pop_d[_number]=float(pop[_number])
    pop_d['a_money']=float(pop['money'])/float(pop['size'])
    availble=True
    try:
        province=rd['province'][pop['province']]
        state=rd['state'][province['state']]
        country=rd['country'][state['country']]
    except KeyError:
        #pop_d['civilized']=np.NaN
        availble=False
    if availble:
        pop_d['civilized']=1 if country['civilized']=='yes' else 0
    else:
        pop_d['civilized']=np.NaN
    return pop_d
    
def get_mat(rd):
    pop_l=[take_pop(rd,pop) for pop in rd['pop'].values()]
    #pop_l=[pop for pop in pop_l if pop['size']>100]
    key_l=pop_l[0].keys()
    dt=pd.DataFrame({key:[pop[key] for pop in pop_l] for key in key_l})
    dt=dt.dropna()
    return dt
    
def sample(path="../SPA1901_09_28.v2"):
    return parse(path)
rd=sample()
    
dt=get_mat(rd)
dt['logam']=np.log(dt['a_money']+0.01)
#dt.applymap(lambda x:np.NaN if abs(x)>10000 else x)
dt=dt.dropna()
#endog=dt['a_money']
endog=dt['logam']
#exog=sm.add_constant(dt[['literacy']+type_l])
exog=sm.add_constant(dt[['civilized']+type_l+religion_l])
mod=sm.OLS(endog,exog)
#mod=sm.RLM(endog,exog,M=sm.robust.norms.HuberT())
res=mod.fit()
print res.summary()