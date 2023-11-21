import cv2
import numpy as np
import os
from PIL import Image


def training():
    data_path = 'dataset'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    users_faces = []
    ids = []
    users = os.listdir(data_path)

    for user in users:
        user_path = os.path.join(data_path, user)
        image_paths = [os.path.join(user_path, f) for f in os.listdir(user_path)]

        for image_path in image_paths:
            PIL_img = Image.open(image_path).convert('L')
            img_np = np.array(PIL_img, np.uint8)

            id = int(os.path.split(user_path)[-1].split('_')[1])
            faces = detector.detectMultiScale(img_np)

            for (x, y, w, h) in faces:
                users_faces.append(img_np[y:y+h, x:x+w])
                ids.append(id)

    print("[INFO] Training...")

    recognizer.train(users_faces, np.array(ids))
    recognizer.write('trainer/trainer.yml')

    print('[INFO] Training {0} face(s) successfully!'.format(len(np.unique(ids))))

