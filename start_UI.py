# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 11:59:29 2016

@author: yiyuezhuo
"""

#from webui.webui import app

#app.run()

import webui.app
#import sys
#import script.cache as cache

#del sys.path[0] #删除本脚本所在的主模块路径，否则数据内建库的select会与本地的那个select.py冲突

webui.app.app.run(debug=True)