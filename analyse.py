# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 16:49:09 2016

@author: Administrator
"""
import os
import re
from select2 import parse
#from collections import defaultdict
import numpy as np
import matplotlib.pylab as plt


def sample(root='../Victoria 2/save games'):
    #root='../Victoria 2/save games'
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


def extract(al,progress=True):
    seq=[]#
    for a in al:
        rd=parse(a['path'])
        if progress:
            print 'load '+a['path']+' succ'
        main_keys=['type','religion']
        wait_keys=['size','money']
        weight_keys=['literacy']
        #dd=defaultdict(lambda:{'size':0.0,'money':0.0})
        sum_dict={mk:{} for mk in main_keys}
        #sum_dict['sum']={wk:0.0 for wk in wait_keys}#sum是直接和，不分类
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
        sur_l=record['sum']['type'].values()
        record['sum']['sum']={sk:sum([sd[sk] for sd in sur_l]) for sk in sur_l[0].keys()}
        record['date']=a['date']
        seq.append(record)
        if progress:
            print 'deal '+a['path']+' succ'
    return seq
    
def T(seq,main_key,sub_key,key):
    #选择出一个序列 如 'type' 'farmer' 'money'
    return [record['sum'][main_key][sub_key][key] for record in seq]
    
def report_detail(seq,main_key,sk,key1,key2):
    axis=[int(record['date'][0]) for record in seq]
    l1=np.array(T(seq,main_key,sk,key1))
    l2=np.array(T(seq,main_key,sk,key2))
    plt.plot(axis,l1/l2)
    plt.show()
    
def report_p(seq,main_key,key1,key2):
    sub_keys=seq[0]['sum'][main_key].keys()
    axis=[int(record['date'][0]) for record in seq]
    for sk in sub_keys:
        print 'plot '+main_key +' '+sk+' '+key1+'/'+key2
        l1=np.array(T(seq,main_key,sk,key1))
        l2=np.array(T(seq,main_key,sk,key2))
        plt.plot(axis,l1/l2)
        plt.show()
        print ' '
def percent_flow(seq,main_key,detail=None,loc=2):
    sub_keys=seq[0]['sum'][main_key].keys()
    d={sk:T(seq,main_key,sk,'size') for sk in sub_keys}
    ds=np.array([sum([sl[i] for sl in d.values()]) for i in range(len(d.values()[0]))])
    axis=[int(record['date'][0]) for record in seq]
    if detail==None:
        for key,value in d.items():
            y=np.array(value)/ds
            plt.plot(axis,y,label=key)
    else:
        for dd in detail:
            y=np.array(d[dd])/ds
            plt.plot(axis,y,label=dd)
    plt.legend(loc=loc)
    plt.show()
    
def report_par(seq,main_key,skl,key1,key2,loc=2):
    axis=[int(record['date'][0]) for record in seq]
    for sk in skl:
        l1=np.array(T(seq,main_key,sk,key1))
        l2=np.array(T(seq,main_key,sk,key2))
        plt.plot(axis,l1/l2,label=sk)
    plt.legend(loc=loc)
    plt.show()

def report(seq):
    report_p(seq,'type','money','size')
    report_p(seq,'type','literacy','size')
    report_p(seq,'religion','money','size')
    report_p(seq,'religion','literacy','size')
    
type_l=['farmers', 'bureaucrats', 'capitalists', 'artisans', 'aristocrats', 'officers', 'clergymen', 'labourers', 'slaves', 'clerks', 'soldiers', 'craftsmen']
religion_l=['shiite', 'catholic', 'mahayana', 'theravada', 'animist', 'orthodox', 'jewish', 'hindu', 'protestant', 'gelugpa', 'shinto', 'coptic', 'sunni', 'sikh']

al=sample()
#seq=test2(al[:3])