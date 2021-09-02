import cv2
import numpy as np
import face_recognition
import os as os
from datetime import datetime
import requests
import psycopg2
import csv
import time
         

path = 'C:/Users/Korisnik/Desktop/projekti/Diplomski_rad/marko/elektronickoposlovanje/faceID/slike'
images = []
classNames = []
myList = os.listdir(path)


for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])



def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print('Kodirana lista' ,encodeList[0])
        print('Duzina matrice: ', len(encodeList[0]), '\n')
    return encodeList




def markAttendance(name, id_studenta):
    
    with open('Attendence.csv','w+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')


            data = {'predavanja_fk': 2, "osoba_fk": id_studenta}
            r =requests.post('http://127.0.0.1:8000/evidencija-create/', json = data)
            


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    succes, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS,facesCurrentFrame)

    for encodeFace,faceLocation in zip(encodeCurrFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDistance)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            name = classNames[matchIndex].lower()
            print(name)
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2), (255,0,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            conn = psycopg2.connect(host='localhost',
                       dbname='elektronickoposlovanjeDB',
                       user='postgres',
                       password='fsre',
                       port='5432')  

            cur = conn.cursor() 
            cur.execute("SELECT id FROM diplomskirad_osobe WHERE email = '{}'".format(name))

            rows = cur.fetchall()
            for row in rows:
                id_studenta = row[0]
                print(row[0])

            markAttendance(name,id_studenta)

        else:
            name = 'Nepoznata osoba'
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    cv2.imshow('Kamera', img)
    key = cv2.waitKey(1)

    if key == 27:
        break