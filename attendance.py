import os

import pyttsx3


Root_Path = os.path.dirname(__file__)

haarcasecade_path = os.path.join(Root_Path,"haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(Root_Path,"TrainingImageLabel\\Trainner.yml")

trainimage_path = os.path.join(Root_Path,"TrainingImage")
studentdetail_path = os.path.join(Root_Path,"StudentDetails\\studentdetails.csv")
attendance_path = os.path.join(Root_Path,"Attendance")

# project module
import show_attendance
import takeImage
import automaticAttendance
import trainImage

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


def main():
    while True:
        print("1. Register")
        print("2 Take Attendance")
        print("3 View Attendance")

        choice = input(("Enter your choice: "))

        if choice == '1':
            EnrollmentNo = int(input("Enter Enrollment Number: "))
            Name = input("Enter Student name: ")
            res = takeImage.TakeImage(
                    EnrollmentNo,
                    Name,
                    haarcasecade_path,
                    trainimage_path,            
                    text_to_speech
                )
            if res == 'Success':
                train = input("Type 'y' if you want to start the training to complete registration: ")
                if train.lower() == 'y':
                    trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path,text_to_speech)

            
        elif choice == '2':
            automaticAttendance.subjectChoose(text_to_speech)
        
        elif choice == '3':
            show_attendance.subjectChoose()

        else:
            print("Invalid Choice")
        
        print()



        

if __name__ == '__main__':
    main()