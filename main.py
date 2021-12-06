from flask import Flask, render_template, Response
from camera import VideoCamera
import face_recognition
import cv2
import numpy as np
import pandas as pd
from datetime import date

import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
        # Load a sample pictures and learn how to recognize it.
    citizen_1 = face_recognition.load_image_file("citizen_pics/emad.jpeg")
    citizen_1_encoding = face_recognition.face_encodings(citizen_1)[0]

    citizen_2 = face_recognition.load_image_file("citizen_pics/barack.jpeg")
    citizen_2_encoding = face_recognition.face_encodings(citizen_2)[0]

    citizen_3 = face_recognition.load_image_file("citizen_pics/elon.jpeg")
    citizen_3_encoding = face_recognition.face_encodings(citizen_3)[0]

    citizen_4 = face_recognition.load_image_file("citizen_pics/jeff.jpeg")
    citizen_4_encoding = face_recognition.face_encodings(citizen_4)[0]
    



    criminal_1 = face_recognition.load_image_file("criminal_pics/elchapo.jpeg")
    criminal_1_encoding = face_recognition.face_encodings(criminal_1)[0]

    criminal_2 = face_recognition.load_image_file("criminal_pics/escobar.jpeg")
    criminal_2_encoding = face_recognition.face_encodings(criminal_2)[0]






    known_face_encodings = [
        citizen_1_encoding,
        citizen_2_encoding,
        citizen_3_encoding,
        citizen_4_encoding,
        criminal_1_encoding,
        criminal_2_encoding
    ]

    known_face_names = [
        "Emad Al Omari",
        "Barack Obama",
        "Elun Musk",
        "Jeff Bezos",
        "Elchapo",
        "Paplo Escobar"
    ]
    while True:
        frame = camera.get_frame(known_face_encodings,known_face_names)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)