import cv2
import os
import asyncio

from service import get_frames
from traning import training


def face_detector(userId):
    done = False
    count = 0
    user_id = 1
    data_path = 'dataset'
    if len(os.listdir(data_path)) != 0:
        user_id = len(os.listdir(data_path)) + 1

    new_dir = "User" + "_" + str(user_id) + "_" + str(userId)
    path = os.path.join(data_path, new_dir)
    os.mkdir(path)

    while True:
        im, gray, faces = asyncio.run(get_frames())

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
            count += 1

            cv2.imwrite(data_path + "/" + new_dir + "/" + str(count) + ".jpg", gray[y:y + h, x:x + w])

            if count > 99:
                ch = int(h / 2)
                cv2.putText(im, "Complete!", (x - 15, y + ch), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 2)
                done = True

        im = cv2.imencode('.jpg', im)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')

        if done:
            training()
            break
