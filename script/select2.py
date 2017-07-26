# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:40:05 2016

@author: yiyuezhuo
"""
from collections import defaultdict

def pure(x):
    try:
        float_x=float(x)
        try:
            int_x=int(x)
            return int_x
        except:
            return float_x
    except:
        return x.strip()
        #return x


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
            if value!='':
                #rd[key.strip()]=value
                rd[key.strip()]=pure(value)
            else:
                key_strip=key.strip()
                #if not(rd.has_key(key_strip)):
                if not key_strip in rd:
                    rd[key_strip]=('block',i)
                else:
                    if type(rd[key_strip][1])!=list:
                        rd[key_strip]=('block',[rd[key_strip][1],i])
                    else:
                        rd[key_strip][1].append(i)
        i+=1
    return rd
    
def take_recursion(sl,index):
    '''All use this function will go a memory hell'''
    rd=take(sl,index)
    trace_l=[]
    for key,value in rd.items():
        if type(value)==tuple and value[0]=='block':
            trace_l.append(key)
    if len(trace_l)==0:
        return rd
    for key in trace_l:
        if type(rd[key][1])!=list:
            recur=take_recursion(sl,rd[key][1])
            rd[key]=recur if len(recur)!=0 else ('block',rd[key][1]) 
        else:
            recurs=[take_recursion(sl,block_index) for block_index in rd[key][1]]
            rd[key]=[recurs[i] if len(recurs[i])!=0 else ('block',rd[key][1][i]) for i in range(len(rd[key][1]))]
    return rd
    
def take_pop(sl,index):
    rd={}
    i=index+2
    level=0
    while True:
        if i==index+4:#fuck paradox
            i+=1
            continue
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
            if value!='':
                #rd[key.strip()]=value
                rd[key.strip()]=pure(value)
            else:
                rd[key.strip()]=('block',i)
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

def is_worldmarket(sl,index):
    return 'worldmarket=' in sl[index] and 'worldmarket' in sl[index+2]
    
def is_state_buildings(sl,index):
    return 'state_buildings=' in sl[index]



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
    #rd=take(sl,index)
    rd=take_pop(sl,index)
    pop.update(rd)
    return pop
    
def country_parse(sl,index):
    country={}
    country['id']=sl[index].split('=')[0].strip()
    rd=take(sl,index)
    country.update(rd)
    for key in pool_keys:
        dummy,index=country[key]
        country[key]=take(sl,index)
    country['bank']=take_recursion(sl,country['bank'][1])
    return country
    
def state_parse(sl,index):
    state={}
    state['id']=sl[index+4].split('=')[1].strip()
    state['type']=sl[index+5].split('=')[1].strip()
    state['provinces']=sl[index+9].split('}')[0].strip().split(' ')
    return state
    
def worldmarket_parse(sl,index):
    '''
    top=take(sl,index)
    market={}
    for key,value in top.items():
        if type(value)==tuple and value[0]=='block':
            market[key]=take(sl,value[1])
        else:
            market[key]=value
    return market
    '''
    return take_recursion(sl,index)
    
def state_buildings_parse(sl,index):
    return take_recursion(sl,index)


def scan(sl):
    '''This return a great dict for province,pop,country,state as a id-label dict'''
    rd={'province':[],'pop':[],'country':[],'state':[]}
    buildings=[]
    worldmarket=None
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
        elif is_worldmarket(sl,i):
            worldmarket=worldmarket_parse(sl,i)
        elif is_state_buildings(sl,i):
            building=state_buildings_parse(sl,i)
            building['_index']=i
            building['state']=rd['state'][-1]['id']
            buildings.append(building)
    rd={tk:{obj['id']:obj for obj in rd[tk]} for tk in rd.keys()}
    #rd={tk:{obj['id']:obj for obj in rd[tk]} for tk in ['province','pop','country','state']}
    rd['worldmarket']=worldmarket
    rd['building']=buildings
    for sta in rd['state'].values():
        for pid in sta['provinces']:
            try:
                pro=rd['province'][pid]
            except KeyError:
                print(sta)
                raise KeyError
            pro['state']=sta['id']
    # 推断pop的国家属性,存在不明遗漏，当前448k，应该不影响大局
    for key,value in rd['pop'].items():
        '''
        try:
            c=rd['state'][rd['province'][[value['province']]]['state']]['country']
        except:
            c=None
        '''
        try:
            province=value['province']
            state=rd['province'][province]['state']
            #try:
            #    state=rd['province'][province]['state']
            #except:
            #    print rd['province'][province]['_index']
            #    raise 'fuck'
            country=rd['state'][state]['country']
            #c=rd['state'][rd['province'][[value['province']]]['state']]['country']
            rd['pop'][key]['country']=country
        except:
            rd['pop'][key]['country']=None
    for bd in rd['building']:
        try:
            state=bd['state']
            country=rd['state'][state]['country']
            bd['country']=country
        except:
            bd['country']=None
    for country in rd['country'].values():
        country['pop_size']=0
    for pop in rd['pop'].values():
        if pop['country']:
            country=rd['country'][pop['country']]
            country['pop_size']+=int(pop['size'])
    return rd


def parse(fname):
    '''
    f=open(fname,'r')
    doc=f.read()
    f.close()
    '''
    with open(fname,'r',encoding='utf8',errors='ignore') as f:
        doc = f.read()
    
    sl=doc.split("\n")
    result=scan(sl)
    return result
    
def parse_buildings(fname):
    '''please pass a building.txt file to get building setting
    . However you can find it in VIC2root/common/buildings.txt
    to get it.'''
    #fname=u'E:\\V2汉化版3.03\\common\\buildings.txt'
    f=open(fname,'r')
    doc=f.read()
    f.close()
    
    ssl=[line.strip() for line in doc.split('\n') if len(line.strip())>0 and line[0]!='#']
    sl=[]
    for line in ssl:
        if line.strip()[-1]=='{' and ('=' in line):
            sl.append(line[:-2])
            sl.append('{')
        else:
            sl.append(line)
    sl.insert(0,'')
    sl.insert(0,'')
    sl.append('}')
    sl.append('')
    sl.append('')
    res=take_recursion(sl,0)
    return res
    
def get_building_price(rd,fname='buildings.txt'):
    bd=parse_buildings(fname)
    for key in bd:
        price=0.0
        for good,value in bd[key]['goods_cost'].items():
            price+=rd['worldmarket']['price_pool'][good]*value
        bd[key]['price']=price
    for building in rd['building']:
        building['value']=bd[building['building'][1:-1]]['price']
    return rd

'''
def to_unicode(s):
    try:
        return unicode(s)
    except UnicodeDecodeError:
        return unicode(s,encoding='gbk')
'''
def to_unicode(s):
    try:
        return s.decode('utf8')
    except UnicodeDecodeError:
        return s.decode('gbk')
def unicode(s):
    return s.decode()

    
def shrink(record):
    # block元组,列表直接删除，子字典将父字典以_拼接合并
    new_record={}
    for key,value in record.items():
        if value ==None:
            continue
        typ=type(value)
        if typ in [list,tuple]:
            continue
        elif typ==dict:
            rv=shrink(value)
            for keyp,valuep in rv.items():
                new_record['__'+key+'__'+keyp]=valuep
        elif typ == str:
            try:
                new_record[key]=unicode(value)
            except UnicodeDecodeError:
                #new_record[key]=unicode(value,encoding='gbk')
                new_record[key]=to_unicode(to_unicode)
        elif typ in [int,unicode,float]:
            new_record[key]=value
        else:
            print(key,value)
            raise 'error'
    return new_record
    
def rd_shrink(rd):
    import pandas as pd
    ddf={}
    for listlike in ['pop','province','state','country']:
        l_l=[shrink(record) for record in rd[listlike].values()]
        #pd.DataFrame(l_l).to_sql(listlike,con)
        ddf[listlike]=pd.DataFrame(l_l)
    #pd.DataFrame([shrink(rd['worldmarket'])]).to_sql('worldmarket',con)
    ddf['worldmarket']=pd.DataFrame([shrink(rd['worldmarket'])])
    return ddf

    
    
def to_sql(rd,connect_path='bignews.db'):
    import pandas as pd
    import sqlite3
    import os
    
    if os.path.isfile(connect_path):
        os.remove(connect_path)
    
    con=sqlite3.connect(connect_path)
    try:
        for listlike in ['pop','province','state','country']:
            l_l=[shrink(record) for record in rd[listlike].values()]
            pd.DataFrame(l_l).to_sql(listlike,con)
        pd.DataFrame([shrink(rd['worldmarket'])]).to_sql('worldmarket',con)
    except Exception as e:
        raise e
    finally:
        con.close()



pool_keys=['domestic_supply_pool','domestic_demand_pool','actual_sold_domestic','saved_country_supply','max_bought']