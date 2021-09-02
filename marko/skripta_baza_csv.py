import psycopg2
import csv
from psycopg2 import sql
import schedule
import time

def push_script():

    conn = psycopg2.connect(host='localhost',
                        dbname='elektronickoposlovanjeDB',
                        user='postgres',
                        password='fsre',
                        port='5432')  

    cur = conn.cursor()

    with open('Zadnji.csv', 'r') as f:

        next(f)
        cur.copy_from(f,'{}'.format('diplomskirad_termini'), sep=',')

    conn.commit()


schedule.every().day.at('07:35').do(push_script)

while True:
    schedule.run_pending()
    time.sleep(1)
