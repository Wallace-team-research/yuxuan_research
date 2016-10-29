from bs4 import BeautifulSoup
import requests

cities = ['01','02','03','04','05','06','07','08','10','11','12','13','15','16','17','18']
URL ='http://www.aepb.gov.cn:8080/WRYJG/STZXGK/'
session = requests.Session()
outfile = open("anhui_info.txt", "w")

starterURL = URL + 'STindex.aspx?dsid=34{}00000000'
for city in cities:
    url = starterURL.format(city)
    req = session.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    links = soup.select("div [class~=jc_list] ul a")
    for link in links:
        entURL = URL + link['href']
        outfile.write(link.string) # entname
        req2 = session.get(entURL)
        soup2 = BeautifulSoup(req2.text, "lxml")
        autoURL = URL + soup2.select('span dd a')[-1]['href']
        outfile.write(" " + autoURL) # auto url
        req3 = session.post(autoURL)
        soup3 = BeautifulSoup(req3.text, "lxml")
        options = soup3.find_all('option')
        for option in options: # all stations
            outfile.write(" " + option['value'])
        outfile.write("\n")

outfile.close()