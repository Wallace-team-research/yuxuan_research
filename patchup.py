import requests
import sqlite3
from data2014 import write_one_company

session = requests.Session()
conn = sqlite3.connect('ShandongCompanyList.db')
cur = conn.cursor()
infile = open("missing_companies.txt", "r")
entname = infile.readline().rstrip('\n')
while entname != '':
    cur.execute('''SELECT EntCode, CityCode, IP, Year FROM CompanyList WHERE EntName=?''',(entname,))
    row = cur.fetchone()
    write_one_company(session,entname,row[0],row[1],row[2],row[3])
    entname = infile.readline().rstrip('\n')
conn.close()