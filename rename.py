import shutil
import sqlite3
import os

conn = sqlite3.connect("ShandongCompanyList.db")
cur = conn.cursor()
cur.execute('''SELECT EntName From CompanyList''')
roster = cur.fetchall()
conn.close()
cwd = os.getcwd()+"/"
for name in roster:
    try:
        shutil.move(cwd+name[0]+".csv", cwd+name[0]+"14.csv")
    except FileNotFoundError:
        continue
