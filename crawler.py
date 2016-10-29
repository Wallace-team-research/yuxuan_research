from rq import Queue
from redis import Redis
from data2014 import write_one_company
import sqlite3
import requests

session = requests.Session()
redis_conn = Redis()
q = Queue(connection=redis_conn, default_timeout=1800)

connR = sqlite3.connect('ShandongCompanyList.db')
curR = connR.cursor()
curR.execute('''SELECT EntName, EntCode, CityCode, IP, Year FROM CompanyList WHERE DONE=1''')
table = curR.fetchall()[221:]
for row in table:
    q.enqueue_call(func=write_one_company,args=(session,row[0],row[1],row[2],row[3],row[4]))
    curR.execute('''UPDATE CompanyList SET DONE=1 WHERE EntCode={}'''.format(row[1]))
    connR.commit()
    row = curR.fetchone()
connR.close()