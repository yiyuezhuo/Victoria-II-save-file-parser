# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:40:05 2016

@author: yiyuezhuo
"""
from collections import defaultdict


def take(sl,index):
    rd={}
    i=index+2
    level=0
    while True:
        line=sl[i]
        if '{' in line:
            level+=1
        if '}' in line:
            level-=1
        if level<0:
            return rd
        if level==0 and '=' in line:
            #print line
            key,value=line.split('=')
            rd[key.strip()]=value
        i+=1
    return rd
    
def is_province(sl,index):
    return '=' in sl[index] and sl[index].split('=')[0].strip().isdigit() and '{' in sl[index+1] and 'name' in sl[index+2]
    
def is_pop(sl,index):
    return '=' in sl[index] and '{' in sl[index+1] and 'id' in sl[index+2] and 'size' in sl[index+3]
    
def is_country(sl,index):
    return '=' in sl[index] and '{' in sl[index+1] and 'tax_base' in sl[index+2]
    
def is_state(sl,index):
    return 'state=' in sl[index] and '{' in sl[index+1] and 'id=' in sl[index+2] 


def province_parse(sl,index):
    province={}
    province['id']=sl[index].split('=')[0].strip()
    rd=take(sl,index)
    province.update(rd)
    return province

def pop_parse(sl,index):
    pop={}
    pop['type']=sl[index].split('=')[0].strip()
    nation,religion=sl[index+4].split('=')
    pop['nation']=nation.strip()
    pop['religion']=religion.strip()
    rd=take(sl,index)
    pop.update(rd)
    return pop
    
def country_parse(sl,index):
    country={}
    country['id']=sl[index].split('=')[0].strip()
    rd=take(sl,index)
    country.update(rd)
    return country
    
def state_parse(sl,index):
    state={}
    state['id']=sl[index+4].split('=')[1].strip()
    state['type']=sl[index+5].split('=')[1].strip()
    state['provinces']=sl[index+9].split('}')[0].strip().split(' ')
    return state


def scan(sl):
    '''This return a great dict for province,pop,country,state as a id-label dict'''
    rd={'province':[],'pop':[],'country':[],'state':[]}
    for i in range(len(sl)-3):
        if is_province(sl,i):
            rd['province'].append(province_parse(sl,i))
            rd['province'][-1]['pop']=[]
            rd['province'][-1]['_index']=i
        elif is_pop(sl,i):
            rd['pop'].append(pop_parse(sl,i))
            rd['pop'][-1]['province']=rd['province'][-1]['id']
            rd['province'][-1]['pop'].append(rd['pop'][-1]['id'])
            rd['pop'][-1]['_index']=i
        elif is_country(sl,i):
            rd['country'].append(country_parse(sl,i))
            rd['country'][-1]['_index']=i
            rd['country'][-1]['state']=[]
        elif is_state(sl,i):
            #print i
            rd['state'].append(state_parse(sl,i))
            rd['state'][-1]['_index']=i
            rd['state'][-1]['country']=rd['country'][-1]['id']
            rd['country'][-1]['state'].append(rd['state'][-1]['id'])
    rd={tk:{obj['id']:obj for obj in rd[tk]} for tk in rd.keys()}
    for sta in rd['state'].values():
        for pid in sta['provinces']:
            try:
                pro=rd['province'][pid]
            except KeyError:
                print sta
                raise KeyError
            pro['state']=sta['id']
    return rd



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


def parse(fname):
    f=open(fname,'r')
    doc=f.read()
    f.close()
    
    sl=doc.split("\n")
    result=scan(sl)
    return result

def test():
    # if you want run the test please unzip the Austria1842_01_12.zip Victoria II game save file
    global rd
    fname="Austria1842_01_12.v2"
    rd=parse(fname)

