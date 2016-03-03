# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 14:09:46 2016

@author: yiyuezhuo
"""

def groupby(l,key,f=None,ff=None):
    if f==None:
        f=lambda x:x

    dd=defaultdict(list)
    for obj in l:
        dd[obj[key]].append(f(obj))
    if ff!=None:
        dd={key:ff(value) for key,value in dd.items()}
    return dd
    
def compare(pl,key,x,y,f=None,x_weight=False,y_weight=False):
    if f==None:
        f=lambda x:x
		
    if x_weight:
        xd=groupby(pl,key,lambda pop:float(pop[x])*float(pop['size']),ff=lambda pop_l:sum(pop_l))
    else:
        xd=groupby(pl,key,lambda pop:float(pop[x]),ff=lambda pop_l:sum(pop_l))
    if y_weight:
        xd=groupby(pl,key,lambda pop:float(pop[x]),ff=lambda pop_l:sum(pop_l))
    else:
        yd=groupby(pl,key,lambda pop:float(pop[y]),ff=lambda pop_l:sum(pop_l))
    
    return {key:f(xd[key],yd[key]) for key in xd.keys()}
    
def groupby_2(l,key1,key2,f=None,ff=None):
    if f==None:
        f=lambda x:x

    dd=defaultdict(list)
    for obj in l:
        dd[(obj[key1],obj[key2])].append(f(obj))
    if ff!=None:
        dd={key:ff(value) for key,value in dd.items()}
    return dd
    
def compare_2(pl,key1,key2,x,y,f=None,x_weight=False,y_weight=False):
    if f==None:
        f=lambda x:x
    
    if x_weight:
        xd=groupby_2(pl,key1,key2,lambda pop:float(pop[x])*float(pop['size']),ff=lambda pop_l:sum(pop_l))
    else:
        xd=groupby_2(pl,key1,key2,lambda pop:float(pop[x]),ff=lambda pop_l:sum(pop_l))
    if y_weight:
        xd=groupby_2(pl,key1,key2,lambda pop:float(pop[x]),ff=lambda pop_l:sum(pop_l))
    else:
        yd=groupby_2(pl,key1,key2,lambda pop:float(pop[y]),ff=lambda pop_l:sum(pop_l))
    
    return {key:f(xd[key],yd[key]) for key in xd.keys()}
    
def test():
    # if you want run the test please unzip the Austria1842_01_12.zip Victoria II game save file
    global rd
    fname="Austria1842_01_12.v2"
    rd=parse(fname)
