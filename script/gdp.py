# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:45:35 2016

@author: yiyuezhuo
"""

import select2
import csv
import pandas as pd

path="../SPA1901_09_28.v2"
text_path='../text.csv'

def sample():
    return select2.get_building_price(select2.parse(path))
def file_l():
    f=open(path)
    sl=f.read().split('\n')
    f.close()
    return sl
def id_to_name():
    f=open(text_path,'r')
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
def get_gdp_sort(rd,name_d=None,display=True,pool_key='domestic_demand_pool'):
    gdp_d={key:get_sum(rd,key,pool_key=pool_key) for key in rd['country'].keys()}
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
    df=pd.DataFrame(rl)
    df['agdp']=df['domestic_demand_pool']/df['pop_size']
    df['p']=df['domestic_supply_pool']/df['domestic_demand_pool']
    return df

def get_agdp(rd):
    df=get_table(rd)
    dl=df.dropna()[['id','agdp']].to_dict('records')
    return {d['id']:d['agdp'] for d in dl}
    
def replace_name(dic,name_d):
    #只是修改dic的key利用name_d
    _dic={}
    for key,value in dic.items():
        try:
            name=name_d[key].decode('gbk')
        except:
            name=key
        _dic[name]=value
    return _dic
def nice_show(dic,name_d=None,sort=True,key=None):
    if key==None:
        key=lambda x:x[1]
    if type(dic)==dict:
        if name_d:
            dic=replace_name(dic,name_d=name_d)
        it=dic.items()
        if sort:
            it.sort(key=key)
        for left,right in it:
            print left,right
    elif type(dic)==pd.core.series.Series:
        nice_show(dic.to_dict(),name_d=name_d,sort=sort,key=key)
        
        
def sort_two_columns(df,key1,key2,name_d=None,sort=True,key=None):
    dl=df.dropna()[[key1,key2]].to_dict('records')
    nice_show({d[key1]:d[key2] for d in dl},name_d=name_d,sort=sort,key=key)
def five_to_table(rd):
    pop_size_d={key:cd['pop_size'] for key,cd in rd['country'].items()}
    five=['saved_country_supply',
         'actual_sold_domestic',
         'max_bought',
         'domestic_demand_pool',
         'domestic_supply_pool']
    pool_d={}
    for pool_key in five:
        pool_d[pool_key]=get_gdp_sort(rd,display=False,pool_key=pool_key)
    df=pd.DataFrame(pool_d)
    df['pop_size']=pd.Series(pop_size_d)
    for pool_key in five:
        df['a'+'_'+pool_key]=df[pool_key]/df['pop_size']
    return df
    
def add_capital(rd,df):
    rs={}
    for cid in rd['country'].keys():
        rs[cid]={'money':rd['country'][cid]['money'],
                'bank':rd['country'][cid]['bank']['money'],
                'lent':rd['country'][cid]['bank']['money_lent'],
                'asset':0.0}
    for bd in rd['building']:
        if bd['country']:
            rs[bd['country']]['asset']+=bd['value']
    return pd.concat([df,pd.DataFrame(rs).T],axis=1)



name_d=id_to_name()
sl=file_l()
rd=sample()
df=five_to_table(rd)
df=add_capital(rd,df)
ddf=df.dropna()
dddf=ddf[['money','bank','asset','lent','actual_sold_domestic','a_actual_sold_domestic']].sort('bank')
#nice_show(get_agdp(rd),key=lambda x:x[1],name_d=name_d)
'''
['saved_country_supply',
 'actual_sold_domestic',
 'max_bought',
 'domestic_demand_pool',
 'domestic_supply_pool']
'''
'''
df=five_to_table(rd)
seq=df.sort('a_actual_sold_domestic')['a_actual_sold_domestic'].dropna()
nice_show(seq.to_dict(),name_d=name_d)
'''