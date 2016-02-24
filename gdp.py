# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:45:35 2016

@author: yiyuezhuo
"""

import select2
import csv
import pandas as pd

path="SPA1901_09_28.v2"

def sample():
    return select2.parse(path)
def file_l():
    f=open(path)
    sl=f.read().split('\n')
    f.close()
    return sl
def id_to_name():
    f=open('text.csv','r')
    l=list(csv.reader(f))
    f.close()
    rd={}
    for line in l:
        #key,value=line[0][:-11].split(';')
        #rd[key]=value
        line=''.join(line)
        if line[0]=='#':
            continue
        ls=line.split(';')
        try:
            key,value=ls[0],ls[1]
        except:
            print line
            raise 'fuck'
        rd[key]=value
    return rd
    
    
def get_sum(rd,country_key,pool_key='domestic_demand_pool'):
    price={key:float(value) for key,value in rd['worldmarket']['price_pool'].items()}
    supply={key:float(value) for key,value in rd['country'][country_key][pool_key].items()}
    #supply={key:float(value) for key,value in rd['country'][country_key]['domestic_supply_pool'].items()}
    r=0.0
    for goods,product in supply.items():
        r+=price[goods]*product
    return r
def get_gdp_sort(rd,name_d=None,display=True):
    gdp_d={key:get_sum(rd,key) for key in rd['country'].keys()}
    if name_d!=None:
        #gdp_d={name_d[key]:gdp for key,gdp in gdp_d.items()}
        gdp_d_={}
        for key,gdp in gdp_d.items():
            try:
                name=name_d[key]
            except:
                print 'miss',key
                name=key
            gdp_d_[name]=gdp
        gdp_d=gdp_d_
    if display:
        gl=sorted(gdp_d.items(),key=lambda x:x[1])
        for key,gdp in gl:
            try:
                key=key.decode('gbk')
            except:
                pass
            print key,gdp
        return
    return gdp_d
    
def get_table(rd):
    href=['tax_base','money','id','pop_size']
    rl=[]
    for key in rd['country'].keys():
        country=rd['country'][key]
        nd={pool_key:get_sum(rd,key,pool_key=pool_key) for pool_key in select2.pool_keys}
        for _key in href:
            nd[_key]=country[_key]
        rl.append(nd)
    return pd.DataFrame(rl)


sl=file_l()
rd=sample()