# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 18:08:48 2016

@author: yiyuezhuo
"""

import cache
import sys

from webui import webui
import sqlite3

#del sys.path[0] #删除本脚本所在的主模块路径，否则数据内建库的select会与本地的那个select.py冲突

'''
db=sqlite3.connect(webui.db_path)

table_names=[c[0] for c in db.execute('select name from sqlite_master where type="table"')]
table_keys={name:list(db.execute('PRAGMA table_info(['+name+'])')) for name in table_names}
'''
rd=cache.RD(webui.db_path)
wm=rd['worldmarket']