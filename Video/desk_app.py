from _thread import start_new_thread
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
import os
import time
import numpy as np
import cv2
import threading
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json
from scipy.ndimage import rotate
import pymysql

# Initialize main window
root = Tk()
root.geometry('780x550+20+20')

# Database connection
con = pymysql.connect(host='localhost', port=3306, user='root', password='123456789', db='autism')
cmd = con.cursor()

# Global variables
flag = False
rec_emotions = []
stu = None  # Ensure stu is globally defined


def ff():
    """Start video playback and emotion detection in separate threads."""
    start_new_thread(ffplay, ())
    start_new_thread(detect_emotion, ())


def st():
    """Stop the application."""
    root.destroy()


def ffplay():
    """Play videos and analyze student emotions."""
    global rec_emotions, flag, stu

    if stu is None:
        print("Error: Student ID (stu) is not set before playing videos.")
        return

    try:
        cmd.execute("SELECT file, id FROM myapp_sm_type_table")
        videos = cmd.fetchall()

        for video in videos:
            flag = True
            video_file = video[0]
            video_id = video[1]

            print(f"Playing video: {video_file}")

            some_command = f"ffplay.exe -autoexit videos/{video_file}"
            p = os.system(some_command)

            flag = False
            pos_cnt = rec_emotions.count("happy") + rec_emotions.count("neutral")
            ratio = pos_cnt / len(rec_emotions) if len(rec_emotions) > 0 else 0

            print(f"Video ID: {video_id}, Ratio: {ratio}")

            # Insert into database with error handling
            try:
                cmd.execute("INSERT INTO `myapp_video_frame` VALUES (NULL, %s, %s, %s)", (video_id, ratio, stu))
                con.commit()
            except Exception as e:
                print(f"Database error: {e}")

            rec_emotions = []  # Reset emotions list for next video

    except Exception as e:
        print(f"Error in ffplay: {e}")


def detect_emotion():
    """Detect emotions from live webcam feed."""
    global rec_emotions, flag

    # Load emotion model
    model = model_from_json(open("model/facial_expression_model_structure.json", "r").read())
    model.load_weights('model/facial_expression_model_weights.h5')

    face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    while True:
        while flag:
            ret, img = cap.read()
            if not ret:
                print("Error: Could not capture image from webcam.")
                continue

            cv2.imwrite("sample.png", img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(f"Detected Faces: {len(faces)}")

            for (x, y, w, h) in faces:
                detected_face = cv2.resize(gray[y:y + h, x:x + w], (48, 48))
                img_pixels = image.img_to_array(detected_face)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels /= 255  # Normalize pixel values

                try:
                    predictions = model.predict(img_pixels)
                    max_index = np.argmax(predictions[0])
                    emotion = emotions[max_index]
                    print(f"Detected Emotion: {emotion}")
                    rec_emotions.append(emotion)
                except Exception as e:
                    print(f"Emotion prediction error: {e}")

                time.sleep(5)  # Wait before next detection

        break

    cap.release()
    cv2.destroyAllWindows()


def student_details():
    """Retrieve and display student details."""
    global stu
    stu = MAPPING.get(box.get())  # Use get() to prevent KeyErrors

    if stu is None:
        print("Error: No student selected!")
        return

    try:
        cmd.execute("SELECT name, dob, gender, place, post, pin, phoneno, email FROM myapp_user_table WHERE id = %s", (stu,))
        s = cmd.fetchone()

        if s:
            Label(root, text="Student Name:").place(relx=0.35, rely=0.30)
            Label(root, text=s[0]).place(relx=0.50, rely=0.30)

            Label(root, text="Place:").place(relx=0.35, rely=0.35)
            Label(root, text=s[3]).place(relx=0.50, rely=0.35)

            Label(root, text="Post:").place(relx=0.35, rely=0.40)
            Label(root, text=s[4]).place(relx=0.50, rely=0.40)

            Label(root, text="Gender:").place(relx=0.35, rely=0.45)
            Label(root, text=s[2]).place(relx=0.50, rely=0.45)

            Label(root, text="DOB:").place(relx=0.35, rely=0.50)
            Label(root, text=s[1]).place(relx=0.50, rely=0.50)

            Label(root, text="Phone No:").place(relx=0.35, rely=0.55)
            Label(root, text=s[6]).place(relx=0.50, rely=0.55)

            Label(root, text="Email:").place(relx=0.35, rely=0.60)
            Label(root, text=s[7]).place(relx=0.50, rely=0.60)
        else:
            print("Error: Student data not found.")

    except Exception as e:
        print(f"Database error: {e}")


# GUI Layout
Label(root, text="SELECT STUDENT").place(relx=0.20, rely=0.25)

cmd.execute("SELECT name, id FROM myapp_user_table")
students = cmd.fetchall()
student_names = [s[0] for s in students]
student_ids = {s[0]: s[1] for s in students}

MAPPING = student_ids  # Store mapping of names to IDs

box_value = StringVar()
box = ttk.Combobox(root, textvariable=box_value, values=student_names, state='readonly')
box.current(0)
box.grid(column=9, row=0, padx=270, pady=140)

Button(root, text="SHOW", command=student_details).place(relx=0.54, rely=0.25)
Button(root, text="START", command=ff).place(relx=0.35, rely=0.65)
Button(root, text="STOP", command=st).place(relx=0.45, rely=0.65)

root.mainloop()
