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
    
class RD_list(object):
    '''这个类模拟rd中的pop列表等,应该是可以迭代的'''
    def __init__(self,bind_path,table_name):
        self.bind_path=bind_path
        self.table_name=table_name
        self.ite=None
        self.head_full=self.once('PRAGMA table_info('+self.table_name+')')
        self.head=[h[1] for h in self.head_full]
        self.head_map={}
        for h in self.head:
            if len(h)>=2 and h[0:2]=='__':
                mid=h.index('__',2)
                block_name=h[2:mid]
                sub_name=h[mid+2:]
                self.head_map[h]=('block',block_name,sub_name)
            else:
                self.head_map[h]=('attr',h)
        self.con=None
    def enhence(self,raw):
        '''数据库直接返回的结果经之前获取的字段名信息等加强返回
        还应该实现当字段有双下划线作为key时把它转成字典形式'''
        d={}
        for i in range(len(self.head)):
            #d[self.head[i]]=raw[i]
            h=self.head[i]
            head_deal=self.head_map[h]
            if head_deal[0]=='block':
                deal,block_name,sub_name=head_deal
                if not(d.has_key(block_name)):
                    d[block_name]={}
                d[block_name][sub_name]=raw[i]
            elif head_deal[0]=='attr':
                deal,attr=head_deal
                d[attr]=raw[i]
        '''
        for key,value in d.items():
            if self.is_block(key):
                block_name,attr_name=self.de_block(key)
                if not(d.has_key(block_name)):
                    d[block_name]={}
                d[block_name][attr_name]=value
            else:
                d[key]=value
        '''
        return d
    def __iter__(self):
        if not(self.ite):
            self.con=sqlite3.connect(self.bind_path)
            #self.ite=iter(self.con.execute('SELECT '+','.join(self.head)+' FROM '+self.table_name))
            self.ite=iter(self.con.execute(self.whole_command()))
        return self
    def whole_command(self):
        selected=' '+','.join(['"'+h+'"' for h in self.head])+' '
        command='SELECT '+selected+' FROM '+self.table_name
        return command
    def next(self):
        try:
            res=self.ite.next()
            return self.enhence(res)
        except StopIteration:
            self.con.close()
            self.con=None
            self.ite=None
            raise StopIteration
    def once(self,command):
        con=sqlite3.connect(self.bind_path)
        res=list(con.execute(command))
        con.close()
        return res
        
class RD_dict(object):
    '''这个表示的是list外面那层字典,主要提供间接访问的,主体仍是RD_list，这个只是wrap'''
    def __init__(self,rd_list):
        self.rd_list=rd_list
        ids=list(rd_list.once('select distinct id from '+rd_list.table_name))
        self.key_list=[iid[0] for iid in ids]
    def keys(self):
        return self.key_list
    def values(self):
        return self.rd_list
    def items(self):
        return [(record['id'],record) for record in self.rd_list]
    def __getitem__(self,key):
        if type(key) in [str,unicode]:
            key='"'+key+'"'
        else:
            key=str(key)
        #command='select '+','.join(self.rd_list.head)+' from '+self.rd_list.table_name+' where id='+key
        command=self.rd_list.whole_command()+' where id='+key
        #print command
        ans=self.rd_list.once(command)
        return self.rd_list.enhence(ans[0])
    
class RD(object):
    '''这个类应该尽可能让数据库像之前直接解析出来的rd一样访问'''
    def __init__(self,bind_path):
        self.bind_path=bind_path
        self.dic={}
        for table_name in ['province','country','state','pop']:
            self.dic[table_name]=RD_dict(RD_list(bind_path,table_name))
        self.dic['worldmarket']=RD_list(bind_path,'worldmarket')
    '''
    def select(self,names,table):
        command='SELECT '+','.join(names)+' FROM '+table
        con=sqlite3.connect(self.bind_path)
        res=list(con.execute(command))
        con.close()
        return res
    '''
    def __getitem__(self,key):
        if key in ['province','country','state','pop']:
            return self.dic[key]
        elif key=='worldmarket':
            return list(self.dic[key])[0]
    
    
#to_sql_all(sample())
#pop_l=RD_list('cache/1836.db','pop')
#country_l=RD_list('cache/1840.db','country')
#country_d=RD_dict(country_l)
    
class Test(object):
    def __init__(self):
        self.ite=iter([1,2,3,4])
    def __iter__(self):
        print '__iter__'
        return self
    def next(self):
        print 'next'
        try:
            res=self.ite.next()
            print 'return',res
            return res
        except StopIteration:
            raise StopIteration

def test2():
    rd=parse('SPA1901_09_28.v2')
    to_sql(rd,connect_path='bignews.db')
    country_l=RD_list('bignews.db','country')
    country_d=RD_dict(country_l)
    country_d['ENG']