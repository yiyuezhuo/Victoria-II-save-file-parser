# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 14:33:45 2016

@author: yiyuezhuo
"""
from select2 import parse,shrink

import pandas as pd
import sqlite3
import os
import re

def sample(root='../Victoria 2/save games'):
    #root='../Victoria 2/save games'
    al=[]
    for name in os.listdir(root):
        r=re.match(r'Korea(\d\d\d\d)_(\d\d)_(\d\d)\.v2',name)
        if r:
            al.append({'path':root+'/'+name,'date':r.groups()})
    al.sort(key=lambda x:x['date'][0])
    return al

def to_sql(rd,connect_path='bignews.db'):
    
    if os.path.isfile(connect_path):
        os.remove(connect_path)
    
    con=sqlite3.connect(connect_path)
    try:
        for listlike in ['pop','province','state','country']:
            l_l=[shrink(record) for record in rd[listlike].values()]
            pd.DataFrame(l_l).to_sql(listlike,con)
        pd.DataFrame([shrink(rd['worldmarket'])]).to_sql('worldmarket',con)
    except Exception,e:
        raise e
    finally:
        con.close()

def to_sql_all(al,cache_path='cache'):
    #接收路径词典列表，使用日期给cache编号
    for a in al:
        date,path=a['date'],a['path']
        year,month,day=date
        rd=parse(path)
        save_path=cache_path+'/'+year+'.db'
        to_sql(rd,connect_path=save_path)
        print 'clear',date
    print 'end'
    
#to_sql_all(sample())