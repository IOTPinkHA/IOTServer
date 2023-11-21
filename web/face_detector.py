import cv2
import os

from service import get_frames
from traning import training


def face_detector(userId):
    count = 0
    user_id = 1
    data_path = 'dataset'
    if len(os.listdir(data_path)) != 0:
        user_id = len(os.listdir(data_path)) + 1

    new_dir = "User" + "_" + str(user_id) + "_" + str(userId)
    path = os.path.join(data_path, new_dir)
    os.mkdir(path)

    while True:
        im, gray, faces = get_frames()

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (104, 126, 255), 2)
            count += 1

            cv2.imwrite(data_path + "/" + new_dir + "/" + str(count) + ".jpg", gray[y:y + h, x:x + w])

        if count > 99:
            training()
            break

        im = cv2.imencode('.jpg', im)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
