# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 18:08:48 2016

@author: yiyuezhuo
"""

import script.cache as cache
import script.select2 as select2
import sys

from webui import app
import sqlite3

#del sys.path[0] #删除本脚本所在的主模块路径，否则数据内建库的select会与本地的那个select.py冲突

'''
db=sqlite3.connect(webui.db_path)

table_names=[c[0] for c in db.execute('select name from sqlite_master where type="table"')]
table_keys={name:list(db.execute('PRAGMA table_info(['+name+'])')) for name in table_names}
'''
rd=cache.RD(app.db_path)
wm=rd['worldmarket']

pool_keys=[u'last_price_history',
 u'last_supply_pool',
 u'price_history',
 u'price_pool',
 u'real_demand',
 u'demand',
 u'actual_sold_world',
 u'supply_pool']