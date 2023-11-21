import os
import urllib.request
import numpy as np
import cv2
from cv2 import data

url = 'http://192.168.1.29/cam-mid.jpg'

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceDetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_TRIPLEX


def get_users():
    data_path = 'dataset'
    users = os.listdir(data_path)
    names = [user.split('_')[-1] for user in users]
    return names


def get_frames():
    img_req = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_req.read()), np.uint8)

    im = cv2.imdecode(img_np, -1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    faces = faceDetector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    return [im, gray, faces]
