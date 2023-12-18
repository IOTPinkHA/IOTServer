import paho.mqtt.client as paho
import cv2
import os
from datetime import datetime
import json

from service import get_users, get_frames, recognizer, font


def recognize_faces():
    client = paho.Client()
    client.connect('broker.mqttdashboard.com', 1883)
    names = get_users()
    if len(os.listdir('trainer')) > 0:
        recognizer.read('trainer/trainer.yml')
    check = False
    while True:
        im, gray, faces = get_frames()

        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        for (x, y, w, h) in faces:
            color = (220, 53, 69)
            cv2.rectangle(im, (x, y), (x + w, y + h), color, 2)

            user_id = 'unknown'
            confidence = ''

            if len(os.listdir('trainer')) > 0:
                user_id, confidence = recognizer.predict(gray[y: y + h, x: x + w])

                if confidence < 80:
                    check = True
                    print(user_id)
                    color = (0, 255, 0)
                    if user_id - 1 < len(names):
                        user_id = names[user_id - 1]
                        data = {
                            "userId": str(user_id),
                            "timeArrival": str(datetime.now().strftime('%d/%m/%Y, %H:%M:%S'))
                        }
                        json_data = json.dumps(data)
                        client.publish('/face-recognition/attendee', json_data, qos=0)
                        cv2.rectangle(im, (x, y), (x + w, y + h), color, 2)
                        confidence = "{0}%".format(round(confidence))
                else:
                    check = False
                    user_id = 'unknown'
                    confidence = ''

            cv2.putText(im, str(user_id), (x, y - 5), font, 1, color, 2)
            cv2.putText(im, str(confidence), (x, y + h - 5), font, 1, color, 2)

            if check:
                ch = int(h / 2)
                cw = int(w / 3)
                cv2.putText(im, "Checked!!!", (x + cw, y + h - 5), font, 1, (255, 0, 0), 2)

        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        im = cv2.imencode('.jpg', im)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')

