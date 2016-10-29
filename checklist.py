import sqlite3

conn = sqlite3.connect("ShandongCompanyList.db")
cur = conn.cursor()
cur.execute(''' SELECT EntName From CompanyList ''')
roster = cur.fetchall()
conn.close()
outfile = open("missing_companies.txt", "w")
for name in roster:
    try:
        infile = open(name[0]+".csv","r")
    except FileNotFoundError:
        outfile.write(name[0]+"\n")
outfile.close()