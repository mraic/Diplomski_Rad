from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from datetime import datetime
import pandas as pd
import re
import psycopg2
import schedule
import time


def posao():

    my_url = 'http://intranet.fsre.sum.ba:81/intranetfsr/teamworks.dll/calendar/calendar1/calendar?'


    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')


    file1 = open('Predmet1.csv', 'w')
    writer1 = csv.writer(file1)


    fnames = ['datum', 'vrijeme_pocetka', 'zavrsetak', 'trajanje']

    with open('Predmet1.csv', mode ='a') as file:
            writer1 = csv.DictWriter(file, fieldnames = fnames)
            writer1.writeheader()



    containers = page_soup.findAll('div', {'class': 'appointment'})

    file = open('Predmet.csv', 'w')
    writer1 = csv.writer(file)


    fnames = ['broj_ucionce_fk_id', 'naziv_kolegija_id', 'studij_fk_id']

    with open('Predmet.csv', mode ='a') as file:
            writer1 = csv.DictWriter(file, fieldnames = fnames)
            writer1.writeheader()


    for container in containers:


                naziv_kolegija = container.div.span.text
                
                broj_ucionice = naziv_kolegija.split(',')
                broj_ucionice = naziv_kolegija.split('(')
                broj_ucionice = broj_ucionice[1]
                broj_ucionice = broj_ucionice[4:7]
                if str('nli') in broj_ucionice:
                    broj_ucionice = '115'
                if str('kvi') in broj_ucionice:
                    broj_ucionice = '115'

                broj_ucionice = int(broj_ucionice)


                conn = psycopg2.connect(host='localhost',
                        dbname='elektronickoposlovanjeDB',
                        user='postgres',
                        password='fsre',
                        port='5432')  

                cur = conn.cursor()
                sql = "SELECT * FROM diplomskirad_ucionica WHERE broj_ucionice = (%(parameter_array)s)"
                cur.execute(sql,{"parameter_array": broj_ucionice})

                rows = cur.fetchall()
                for row1 in rows:
                    continue
                    #print(row[0])
        

                ime_kolegija = container.div.span.text
                test = ime_kolegija.split(',')
                test = ime_kolegija.split('(')
                del test[1:]
                predmeti = ''.join([str(elem) for elem in test])
                predmeti = predmeti[:-1]
                

                cur = conn.cursor()
                sql = "SELECT id FROM public.diplomskirad_kolegiji WHERE naziv_kolegija = %(parameter_array)s" 

                cur.execute(sql,{'parameter_array':predmeti})

                rows = cur.fetchall()
                
                for row in rows:
                    continue
                
                with open('Predmet.csv', mode ='a') as file:
                    writer1 = csv.DictWriter(file, fieldnames = fnames)

                    fnames1 = ['broj_ucionce_fk_id', 'naziv_kolegija_id', 'studij_fk_id']
                    writer1 = csv.DictWriter(file, fieldnames = fnames)
                    writer1.writerow({'broj_ucionce_fk_id': row1[0], 'naziv_kolegija_id': row[0],'studij_fk_id':1})
                #conn.close()           

            
                

    divs = page_soup.select('.appointment > div.h4 > span')

    styles = page_soup.select('.appointment[style]')
    scripts = page_soup.select('script')
    lines = scripts[18].string.split("\n")


    for idx, line in enumerate(lines):
        if line.startswith("FActivityArray") and "[\"id\"]" in line:
            id = line.replace(";", "").split(
                " = ")[1].replace("\"", "").replace("\r", "")
            
            startDateTime = lines[idx + 5].replace(";", "").split(
                " = ")[1].replace("\"", "").replace("\r", "")
            
            endDateTime = lines[idx + 4].replace(";", "").split(
                " = ")[1].replace("\"", "").replace("\r", "")
            
            startDateTime = datetime.strptime(startDateTime, "%Y-%m-%d,%H:%M:%S")
            
            month = startDateTime.month
            day = startDateTime.day
            startDateTime2 = str(day) + "."+str(month)
            endDateTime = datetime.strptime(endDateTime, "%Y-%m-%d,%H:%M:%S")

            trajanje = endDateTime - startDateTime
            trajanje_lista = [trajanje]

            vrijeme_pocetka = []
            vrijeme_pocetka.append(startDateTime)
            
            zavrsni_datum = []
            zavrsni_datum.append(endDateTime)

            fnames = ['datum', 'vrijeme_pocetka', 'zavrsetak', 'trajanje']

            with open('Predmet1.csv', mode ='a') as file:
                writer1 = csv.DictWriter(file, fieldnames = fnames)

                for i in vrijeme_pocetka:
                    for j in zavrsni_datum:
                    
                    
                        writer1.writerow({'datum':datetime.strftime(i, "%Y-%m-%d"),\
                            'trajanje': trajanje,\
                            'vrijeme_pocetka':datetime.strftime(i, "%H:%M:%S"),\
                            'zavrsetak':datetime.strftime(j, "%H:%M:%S"),\
                        })

            

    file.close()
    data1 = pd.read_csv('Predmet1.csv')
    data2 = pd.read_csv('Predmet.csv')
    combined_csv = pd.concat([data1,data2],axis=1)

    combined_csv.to_csv("combined.csv",index='True', encoding='utf-8-sig')

    with open('combined.csv',newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        
    with open('combined.csv','w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['id','datum', 'vrijeme_pocetka', 'zavrsetak', 'trajanje','broj_ucionce_fk_id','naziv_kolegija_id','studij_fk_id'])
        w.writerows(data)

    df = pd.read_csv('combined.csv')
    df1 = df.drop(index = 0, axis = 0)
    df1.to_csv('Zadnji.csv',index=False)

schedule.every().day.at('18:30').do(posao)

while True:
    schedule.run_pending()
    time.sleep(1)