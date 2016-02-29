# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 12:01:30 2016

@author: yiyuezhuo
"""

import os
import sqlite3
#import sys
from flask import (
    Flask, abort, escape, flash, make_response, Markup, redirect,
    render_template, request, url_for)

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
print 'CUR_DIR',CUR_DIR

#db_path=os.path.join(CUR_DIR,'..','cache','1836.db')#这100个序列文件还没有进行__标示化
db_path=os.path.join(CUR_DIR,'..','bignews.db')
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