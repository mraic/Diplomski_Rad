from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import csv

my_url = 'http://intranet.fsre.sum.ba:81/intranetfsr/teamworks.dll/calendar/calendar5/calendar?ShowSysMessages=true&urlencUTF8=true'


uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser')

containers = page_soup.findAll('div',{'class':'appointment'})

file = open('Predmet.csv','w')
writer = csv.writer(file)

writer.writerow(['naziv_kolegija'])

for container in containers:
    naziv_kolegija = container.div.span.text

    print(naziv_kolegija)
    writer.writerow([naziv_kolegija.encode('utf-8')])



file.close()