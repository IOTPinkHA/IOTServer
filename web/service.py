import os
import numpy as np
import cv2
from cv2 import data
from io import BytesIO
from PIL import Image
from websockets import client

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceDetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_TRIPLEX


def get_users():
    data_path = 'dataset'
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    users = os.listdir(data_path)
    names = [user.split('_')[-1] for user in users]
    return names


async def get_frames():
    async with client.connect("ws://192.168.1.23:60") as socket:
        img_req = await socket.recv()
        im = Image.open(BytesIO(img_req))

        im = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

        faces = faceDetector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        return [im, gray, faces]
