# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 12:01:30 2016

@author: yiyuezhuo
"""
import sys
print(sys.path)

from webui.config import CUR_DIR,db_path
import os
import sqlite3
import script.cache as cache
import json
import chart_backend
#import jinja2
#import sys
from flask import (
    Flask, abort, escape, flash, make_response, Markup, redirect,
    render_template, request, url_for)

#CUR_DIR = os.path.realpath(os.path.dirname(__file__))
print('CUR_DIR',CUR_DIR)

#db_path=os.path.join(CUR_DIR,'..','cache','1836.db')#这100个序列文件还没有进行__标示化
#db_path=os.path.join(CUR_DIR,'..','bignews.db')
def query(command):
    con=sqlite3.connect(db_path)
    res=list(con.execute(command))
    con.close()
    return res
def select(table,keys,return_type='record'):
    command='SELECT '+','.join(['"'+key+'"' for key in keys])+ ' FROM '+table
    res=query(command)
    if return_type=='record':
        rdl=[{keys[i]:record[i] for i in range(len(keys))} for record in res]
        return rdl
    elif return_type=='column':
        return res
    
def VIC2_db_query():
    focus=['id','money','type']
    pop_l=select('pop',focus)
    return pop_l
    
    


app = Flask(
    __name__,
    static_folder=os.path.join(CUR_DIR, 'static'),
    template_folder=os.path.join(CUR_DIR, 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/table2')
def table2():
    datas=VIC2_db_query()
    cols=datas[0].keys()
    return render_template('table2.html',cols=cols,datas=datas)

@app.route('/market')
def market():
    rd=cache.RD(db_path)
    wm=rd['worldmarket']
    #goods contain 48 goods
    tables={}
    for key,table in wm.items():
        if type(table)==dict and len(table)==48:
            tables[key]=table
    goods_keys=tables.values()[0].keys()
    pool_keys=tables.keys()
    rdl=[]
    for good_key in goods_keys:
        row={'good':good_key}
        for pool_key in pool_keys:
            row[pool_key]=tables[pool_key][good_key]
        rdl.append(row)
    cols=['good']+pool_keys
    datas=rdl
    return render_template('table2.html',cols=cols,datas=datas)

@app.route('/country')    
def country():
    '''
    rd=cache.RD(db_path)
    price_pool=rd['worldmarket']['price_pool']
    supply_pool=rd['country']['ENG']['domestic_supply_pool']
    #print supply_pool
    gdp_d={good:price_pool[good]*value for good,value in supply_pool.items() if value != None}
    good_name_string=json.dumps(gdp_d.keys()).replace('"','&#34')
    good_list_string=json.dumps([{'name':good,'value':value} for good,value in gdp_d.items()])
    #print good_name_string
    #print good_list_string
    '''
    return render_template('country.html')
    '''
    return render_template('country.html',
                           good_name_string=json.encoder.encode_basestring(good_name_string),
                           good_list_string=json.encoder.encode_basestring(good_list_string))
    return render_template('country.html',good_name_string=good_name_string,
                           good_list_string=good_list_string)
    '''

@app.route('/JSON')    
def getJSON():
    params=request.args
    print (request.args)
    if not(params.has_key('file_name') and params.has_key('func_name')):
        return 'Error'
    else:
        file_name=params['file_name']
        func_name=params['func_name']
        kwarg={}
        for key in['pool_key','country_id']:
            if params.has_key(key):
                kwarg[key]=params[key]
        '''
        if params.has_key('pool_key'):
            kwarg['pool_key']=params['pool_key']
        if params.has_key('country_id']):
            kwarg['country_id']=params['country_id']
        '''
        print(kwarg)
        chart_backend.render(file_name,**kwarg)
        f=open('webui/tmp/'+file_name,'r')
        s=f.read()
        f.close()
        rs=func_name+'('+s+')'
        return rs
        