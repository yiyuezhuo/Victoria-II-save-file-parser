# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 13:32:20 2016

@author: yiyuezhuo
"""
import script.cache as cache
from webui.config import CUR_DIR,db_path
import json



def get_pie(country_id='ENG',pool_key='domestic_supply_pool'):
    rd=cache.RD(db_path)
    price_pool=rd['worldmarket']['price_pool']
    supply_pool=rd['country'][country_id][pool_key]
    gdp_d={good:price_pool[good]*value for good,value in supply_pool.items() if value != None}
    #good_name_string=json.dumps(gdp_d.keys())
    #good_list_string=json.dumps([{'name':good,'value':value} for good,value in gdp_d.items()])
    res={'good_name':gdp_d.keys(),
         'good_list':[{'name':good,'value':value} for good,value in gdp_d.items()],
         'country_id':country_id,
         'pool_key':pool_key}
    return res

def render(file_name,**kwarg):
    if file_name=='pie.json':
        option={'title':{'text':None,'subtext':None},
                'legend':{'data':None},
                'series':{'name':None,'data':None}}
        res=get_pie(**kwarg)
        option['title']['text']=res['country_id']
        option['title']['subtext']=res['pool_key']
        option['legend']['data']=res['good_name']
        option['series']['name']=res['good_name']
        option['series']['data']=res['good_list']
        f=open('webui/tmp/'+file_name,'w')
        f.write(json.dumps(option))
        f.close()
        return
    print '***'
    print 'file_name',file_name
    print '***'
    raise Exception('Not have this name handler')