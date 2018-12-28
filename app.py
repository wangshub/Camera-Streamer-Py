#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_frame():
    # TODO: list all camera devices, default device is 0
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    while True:
        ret, im = camera.read()
        img_encode = cv2.imencode('.jpg', im)[1]
        img_string_data = img_encode.tostring()
        yield (b'--frame\r\n' 
               b'Content-Type: text/plain\r\n\r\n' + img_string_data + b'\r\n')


@app.route('/video')
def calc():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)