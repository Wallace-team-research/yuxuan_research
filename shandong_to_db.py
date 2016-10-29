# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 00:59:22 2016

@author: Bluefish_
A spider to extract the list of all companies on Shandong's website
Put them into a sqlite3 database. 
"""

import requests
import json
import sqlite3

def get_response(year, page):
    ''' Passing headers extracted from Chrome Inspect Network Tab to get response '''
    url_to_request = 'http://58.56.98.78:8405/ajax/npublic/Index.ashx?jsoncallback=jQuery1111026710970292811953_1475289728500'
    form_data = {'IsBeginZxjc':'1', # has CEMS
             'Method':'LoadGrid',
             'SubType':'0', # emit air pollutants
             'Year':year,
             'areaCode':'0', # all
             'cityCode':'0', # all
             'EntName':'',
             'page':page,
             'rows':'40'}
    headers = {'Host': '58.56.98.78:8405',
           'Connection': 'keep-alive',
           'Content-Length': '95',
           'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
           'Origin': 'http://58.56.98.78:8405',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Referer': 'http://58.56.98.78:8405/',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
           'Cookie': 'ASP.NET_SessionId=hwkfbkzrlcugfmotu00ghdxc'}
    session = requests.Session()
    req = session.post(url_to_request, data=form_data, headers=headers)
    return req.content.decode('utf-8')
                
def write_to_sqlite():
    ''' write the company data to an sqlite3 database '''
    
    city_to_ip = {'济南':'119.164.252.34:8403',
                  '青岛':'219.147.6.195:8403',
                  '淄博':'60.210.111.130:8406',
                  '枣庄':'218.56.152.39:8403',
                  '东营':'221.2.232.50:8401',
                  '烟台':'218.56.33.245:8403',
                  '潍坊':'122.4.213.20:8403',
                  '济宁':'60.211.254.236:8403',
                  '泰安':'220.193.65.234:8403',
                  '威海':'60.212.191.18:8408',
                  '日照':'219.146.185.5:8404',
                  '莱芜':'218.56.160.167:8403',
                  '临沂':'58.57.43.244:8414',
                  '德州':'222.133.11.150:8403',
                  '聊城':'222.175.25.10:8403',
                  '滨州':'222.134.12.94:8403',
                  '菏泽':'219.146.175.226:8403'}    
    
    connection = sqlite3.connect("ShandongCompanyList.db")
    cur = connection.cursor()
    cur.execute('''DROP TABLE IF EXISTS CompanyList''')
    cur.execute('''CREATE TABLE CompanyList (EntName TEXT, CityName TEXT, AreaName TEXT, 
    AreaCode TEXT, CityCode TEXT, EntTypeName TEXT, EntCode TEXT UNIQUE, IP TEXT, Year TEXT)''')
    year_pages = {'2014':15, '2015':28, '2016':28}    
    
    for year, page in year_pages.items():
        for i in range(page):
            response = get_response(year, str(i+1))          
            response = response[response.find('(')+1 : -1]
            json_res = json.loads(response)
            table = json_res['rows']
            for entry in table:
                en = entry['EntName']
                cn = entry['CityName']
                an = entry['AreaName']
                ac = entry['AreaCode']
                cc = entry['CityCode']
                etn = entry['EntTypeName']
                ec = entry['EntCode']
                ip = city_to_ip[cn]
                cur.execute('''INSERT OR IGNORE INTO CompanyList (EntName, 
                CityName, AreaName, AreaCode, CityCode, EntTypeName, EntCode, 
                IP, Year) VALUES (?,?,?,?,?,?,?,?,?)''', (en,cn,an,ac,cc,etn,ec,ip,year))
    
    connection.commit()
    connection.close()

write_to_sqlite()