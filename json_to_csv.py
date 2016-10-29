import json
import csv

companyname = input("Enter company name:")

infile = open(companyname+".json", "r")
string = infile.read()
infile.close()
string = string[:-1]
string = "["+string+"]"
file_to_write = open(companyname+'.csv', 'w')
csvfile = csv.writer(file_to_write)
table = json.loads(string)
csvfile.writerow([k for k in table[0].keys()])
for entry in table:
    csvfile.writerow([v for v in entry.values()])
file_to_write.close()