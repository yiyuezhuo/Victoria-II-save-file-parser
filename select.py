# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#from itertools import groupby
from collections import defaultdict

test_file_name="Austria1842_01_12.v2"
f=open(test_file_name,'r')
doc=f.read()
f.close()

sl=doc.split("\n")

def scan(sl,start_index,match,start="{",end="}"):
    level=0
    result=[]
    i=start_index
    while True:
        line=sl[i]
        if start in line:
            level+=1
        if end in line:
            level-=1
        if level<0:
            return result
        if level==0:
            if match in line:
                result.append(i)
        i+=1
    raise '?'
    
def select(sl,seq,start_index=0):
    cut_tree=[[start_index]]
    for sign in seq:
        live=cut_tree[-1]
        build=[]
        for new_start_index in live:
            r=scan(sl,new_start_index+2,sign)
            build.extend(r)
        cut_tree.append(build)
    return cut_tree
    
def pop_select(sl):
    result=[]
    for i in range(len(sl)-3):
        line1=sl[i+1]
        line2=sl[i+2]
        line3=sl[i+3]
        if '{' in line1 and 'id' in line2 and 'size' in line3:
            result.append(i)
    return result
    
def pop_pure(pop):
    pop['bank']=pop.get('bank',0.0)
    return pop
    
def pop_parse(sl,index):
    pop={}
    pop['type']=sl[index].split('=')[0].strip()
    nation,religion=sl[index+4].split('=')
    pop['nation']=nation.strip()
    pop['religion']=religion.strip()
    i=index+2
    level=0
    while True:
        line=sl[i]
        if '{' in line:
            level+=1
        if '}' in line:
            level-=1
        if level<0:
            return pop_pure(pop)
        if level==0 and '=' in line:
            #print line
            key,value=line.split('=')
            pop[key.strip()]=value
        i+=1
    return pop
    
def pop_l_parse(sl):
    index_l=pop_select(sl)
    return [pop_parse(sl,index) for index in index_l]
    
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


    
    
def test(sl):
    pl=pop_select(sl)
    pop_l=[pop_parse(sl,pop_index) for pop_index in pl]
    gb=defaultdict(list)
    for pop in pop_l:
        gb[pop['type']].append(pop)
    return gb
    

'''
#result=scan(sl,1315423,'ENG')
result=scan(sl,0,'ENG')
print result

rd=test(sl)
rd_money={key:sum([float(pop['money']) for pop in value]) for key,value in rd.items()}
rd_size={key:sum([float(pop['size']) for pop in value]) for key,value in rd.items()}
'''
pl=pop_l_parse(sl)
type_money=compare(pl,'type','money','size',f=lambda x,y:x/y)
print type_money