
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
    c1 = face_recognition.load_image_file("citizen_database/emad.jpeg")
    c1_encoding = face_recognition.face_encodings(c1)[0]

    c2 = face_recognition.load_image_file("citizen_database/barack.jpeg")
    c2_encoding = face_recognition.face_encodings(c2)[0]

    c3 = face_recognition.load_image_file("citizen_database/elon.jpeg")
    c3_encoding = face_recognition.face_encodings(c3)[0]

    c4 = face_recognition.load_image_file("citizen_database/jeff.jpeg")
    c4_encoding = face_recognition.face_encodings(c4)[0]
    



    cr2 = face_recognition.load_image_file("criminal_database/elchapo.jpeg")
    cr2_encoding = face_recognition.face_encodings(cr2)[0]

    cr3 = face_recognition.load_image_file("criminal_database/escobar.jpeg")
    cr3_encoding = face_recognition.face_encodings(cr3)[0]






    known_face_encodings = [
        c1_encoding,
        c2_encoding,
        c3_encoding,
        c4_encoding,
        cr2_encoding,
        cr3_encoding
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
