# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 16:49:09 2016

@author: Administrator
"""
import os
import re
from select2 import parse
from collections import defaultdict


def sample():
    root='../Victoria 2/save games'
    al=[]
    for name in os.listdir(root):
        r=re.match(r'Korea(\d\d\d\d)_(\d\d)_(\d\d)\.v2',name)
        if r:
            al.append({'path':root+'/'+name,'date':r.groups()})
    al.sort(key=lambda x:x['date'][0])
    return al

'''
1853重复
缺1855
缺1918
'''
def test(al):
    global money_seq,size_seq
    money_seq=[]
    size_seq=[]
    for a in al:
        rd=parse(a['path'])
        print 'load '+a['path']+' succ'
        money_t=0.0
        size_t=0.0
        for pop in rd['pop'].values():
            money_t+=float(pop['money'])
            size_t+=float(pop['size'])
        money_seq.append(money_t)
        size_seq.append(size_t)
        
def extract(rd,type_key,keys):
    #将rd以type_key对各keys求和
    rrd={key:0.0 for key in keys}
    for pop in rd['pop'].values():
        for key in keys:
            rrd[key]+=float(pop[key])
    return rrd
        
def test2(al):
    seq=[]#stat是汇总字典，这里应该返回各个
    for a in al:
        rd=parse(a['path'])
        print 'load '+a['path']+' succ'
        main_keys=['type','religion']
        wait_keys=['size','money']
        weight_keys=['literacy']
        #dd=defaultdict(lambda:{'size':0.0,'money':0.0})
        sum_dict={mk:{} for mk in main_keys}
        record={'pop_number':len(rd['pop'].values()),'sum':sum_dict}
        for pop in rd['pop'].values():
            for mk in main_keys:
                tk=pop[mk]
                if not(record['sum'][mk].has_key(tk)):
                    record['sum'][mk][tk]={k:0.0 for k in wait_keys+weight_keys}
                for wk in wait_keys:
                    record['sum'][mk][tk][wk]+=float(pop[wk])
                for wk in weight_keys:
                    record['sum'][mk][tk][wk]+=float(pop[wk])*float(pop['size'])
                    #record['sum'][mk][wk]+=float(pop[wk])
        record['date']=a['date']
        seq.append(record)
        print 'deal '+a['path']+' succ'
    return seq
        
        
al=sample()
seq=test2(al[:3])