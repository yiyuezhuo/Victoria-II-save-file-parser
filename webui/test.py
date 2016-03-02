# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 18:08:48 2016

@author: yiyuezhuo
"""

import webui
import sqlite3

from script import cache
'''
db=sqlite3.connect(webui.db_path)

table_names=[c[0] for c in db.execute('select name from sqlite_master where type="table"')]
table_keys={name:list(db.execute('PRAGMA table_info(['+name+'])')) for name in table_names}
'''
rd=cache.RD(webui.db_path)
#wm=rd.worldmarket