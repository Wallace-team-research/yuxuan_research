# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 15:17:04 2016

@author: Bluefish_
A spider that crawls the data of one specific company
P.S. only data in 2014.
"""

import requests
import sqlite3
import json
import random

def create_URL(EntCode, IP, yr):
    starter = 'jQuery11110' + str(int(random.random()*1e17))+'_1457362'
    rand = int(random.random()*1e6)
    paramkeys = ['jsoncallback','Method','entCode','subType','subID',
                 'year','itemCode','dtStart','dtEnd','monitoring',
                 'bReal','page','rows','_']
    paramvals = [starter+str(rand),'GetMonitorDataList',EntCode,'',
                '26264',yr,'','2014-01-01','2014-12-31','1','false',
                '{}','500','1457362'+str(rand+101)]
    key_value = [k+'='+v for (k,v) in zip(paramkeys, paramvals)]
    starterURL='http://'+IP+'/ajax/npublic/NData.ashx?'
    return starterURL + '&'.join(key_value)

def write_one_company(session,en,ec,cc,ip,yr):
    p = 1
    response = ""
    template_url = create_URL(ec, ip, yr)
    output = open(en+"14.json", "w")
    output.write("[")
    while True:
        try: 
            response = session.get(template_url.format(str(p))).text 
        except requests.exceptions.ConnectionError:
            print(template_url.format(str(p)))
        if len(response) < 80:
            break;
        response = response[response.find('[')+1 : -3]
        if p!=1:
            output.write(","+response)
        else:
            output.write(response)
        p += 1
    output.write("]")
    output.close()
