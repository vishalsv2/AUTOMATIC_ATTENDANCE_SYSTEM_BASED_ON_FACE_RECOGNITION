import os

from attendance import attendance_path

def subjectChoose():
    subject = input("Enter subject: ")
    os.startfile(os.path.join(attendance_path,subject))

