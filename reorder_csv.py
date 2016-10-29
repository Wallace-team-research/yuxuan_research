import csv
import _csv

fieldnames = ["Ac005_datetime", "Ac005_cbbs", "Stander", "Typecode", 
            "Mfrequency", "Itemname", "Ac005_value", "Subname", "Subid", 
            "Itemcode", "Ac004_pid", "Pid"]
emptyfields = ["Subid", "Itemcode", "Ac004_pid", "Pid"]
itemnames = [u'氨氮', u'二氧化硫', u'化学需氧量', u'氮氧化物', 
             u'颗粒物', u'烟尘']

def write_reordered_csv(entname):
    infile = open(entname+"14.csv", "r")
    outfile = open("2014/"+entname+"2014.csv", "w")
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv.DictReader(infile):
        writer.writerow(row)
    infile.close()
    outfile.close()

rosterfile = open("noheader.txt", "r")
entname = rosterfile.readline().rstrip("\n")
while entname!='':
    infile = open(entname+"14.csv", "r")
    row = infile.readline().rstrip('\n')
    while row.find("--")<0:
        row = infile.readline().rstrip('\n')
    row = row.split(",")
    counter = 0
    fields = []
    for item in row:
        if item=='':
            fields.append(emptyfields[counter])
            counter += 1
        elif item==u'2小时/次':
            fields.append("Mfrequency")
        elif item==u'自动':
            fields.append("Typecode")
        elif item.find(':')>-1:
            fields.append("Ac005_datetime")
        elif item=="--":
            fields.append("Ac005_cbbs")
        elif item in itemnames:
            fields.append("Itemname")
        elif item.find(".")>-1:
            fields.append("Ac005_value")
        else:
            try:
                int(item)
            except ValueError:
                fields.append("Stander")
            else:
                fields.append("Subname")
    infile.seek(0)
    content = infile.read()
    infile.close()
    infile = open(entname+"14.csv", "w")
    infile.write(",".join(fields)+"\n")
    infile.write(content)
    infile.close()
    write_reordered_csv(entname)
    entname = rosterfile.readline().rstrip("\n")