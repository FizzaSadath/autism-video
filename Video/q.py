
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
from keras.preprocessing import image
from scipy.ndimage import rotate

root=Tk()
root.geometry('780x550+20+0')
import pymysql
# -----------------------------
# face expression recognizer initialization
from keras.models import model_from_json

model = model_from_json(open("model/facial_expression_model_structure.json", "r").read())
model.load_weights('model/facial_expression_model_weights.h5')  # load weights

face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)


emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
i=0

while(True):

        ret, img = cap.read()

        # img = cv2.imread('../11.jpg')
        # cv2.imwrite(str(i)+".jpg",img)
        i=i+1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #print(faces) #locations of detected faces
        emotion=None

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image

            detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis = 0)

            img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

            predictions = model.predict(img_pixels) #store probabilities of 7 expressions

            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[max_index]
            # rec_emotions.append(emotion)
            print (emotion)
            # time.sleep(5)

            # if cv2.waitKey(1):
        cv2.imshow('img', img)

        # if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        #     break

        # kill open cv things
cap.release()
cv2.destroyAllWindows()