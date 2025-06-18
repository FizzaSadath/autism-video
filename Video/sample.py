# from datetime import timedelta,date
# import calendar
# import datetime
#
# def daterange(d1,d2):
#     for n in range(int((d2-d1).days)+1):
#         yield d1+timedelta(n)
# sd=date(2020,2,16)
# ed=date(2020,2,28)
# for dt in daterange(sd,ed):
#     s=dt.strftime("%Y-%m-%d")
#
#     b=datetime.datetime.strptime(s,'%Y-%m-%d').weekday()
#     ss=calendar.day_name[b]
#     print(s,"=",ss.lower())

#
# from os import walk
# import os
#
# import numpy as np
#
# from src.featureextract import glcm_feat
#
#
# def train():
#     data=[]
#     samples=[]
#     names=[]
#     for dir,d_path,filnames in walk("static/autistic"):
#       for file in filnames:
#           sample=glcm_feat(os.path.join(dir,file))
#           names.append(1)
#           samples.append(sample)
#     for dir,d_path,filnames in walk("static/non_autistic"):
#           for file in filnames:
#             sample=glcm_feat(os.path.join(dir,file))
#             names.append(2)
#             samples.append(sample)
#     np.savetxt("sample.data",samples)
#     np.savetxt("labels.data",names)
# train()




from tensorflow.keras.models import model_from_json


import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import time

model = model_from_json(open("model/facial_expression_model_structure.json", "r").read())
model.load_weights('model/facial_expression_model_weights.h5')  # load weights


face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

rec_emotions=[]
emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
i=0
global flag
while(True):
    ret, img = cap.read()
    cv2.imwrite("sample.png",img)

    # img = cv2.imread('../11.jpg')
    # cv2.imwrite(str(i)+".jpg",img)
    i=i+1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(len(faces),"=========================================")

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
        try:
            predictions = model.predict(img_pixels) #store probabilities of 7 expressions

            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[max_index]
            print(emotion,"==============================================")
            rec_emotions.append(emotion)
            print (emotion)
        except Exception as e:
            print(e,"+++++++++++++++++++++++++++=")
            print(e,"+++++++++++++++++++++++++++=")
            print(e,"+++++++++++++++++++++++++++=")
        time.sleep(5)