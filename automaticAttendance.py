import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
import pandas as pd
import datetime
import time

from attendance import haarcasecade_path, trainimagelabel_path, studentdetail_path, attendance_path


def subjectChoose(text_to_speech):
    subject = input("Enter Subject: ")
    now = time.time()
    future = now + 20

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(trainimagelabel_path)
    except:
        err = "Model not found, please train model"
        text_to_speech(err)
    else:
        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        while True:
            ___, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                global Id

                Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                if conf < 70:
                    print(conf)
                    print(Id)
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime(
                        "%Y-%m-%d"
                    )
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                        "%H:%M:%S"
                    )
                    aa = df.loc[df["Enrollment"] == Id]["Name"].values
                    global tt
                    tt = str(Id) + "-" + aa
                    # En='1604501160'+str(Id)
                    attendance.loc[len(attendance)] = [
                        Id,
                        aa,
                    ]
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                    cv2.putText(
                        im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                    ) 
                else:
                    Id = "Unknown"
                    tt = str(Id)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                    cv2.putText(
                        im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                    )           
            if time.time() > future:
                break

            attendance = attendance.drop_duplicates(
                ["Enrollment"], keep="first"
            )
            cv2.imshow("Filling Attendance...", im)
            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break     
        ts = time.time()
        print(aa)
        # attendance["date"] = date
        # attendance["Attendance"] = "P"
        attendance[date] = 1
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Hour, Minute, Second = timeStamp.split(":")
        # fileName = "Attendance/" + Subject + ".csv"
        path = os.path.join(attendance_path, subject)
        fileName = (
            f"{path}/"
            + subject
            + "_"
            + date
            + "_"
            + Hour
            + "-"
            + Minute
            + "-"
            + Second
            + ".csv"
        )
        attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
        print(attendance)
        attendance.to_csv(fileName, index=False)

        m = "Attendance Filled Successfully of " + subject
        print(m)
        text_to_speech(m)        

        cam.release()
        cv2.destroyAllWindows()