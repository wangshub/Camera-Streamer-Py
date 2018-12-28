#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import queue
import threading

q_camera_frame = queue.Queue(maxsize=10)

app = Flask(__name__)


@app.route('/')
def index():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_frame():
    while True:
        img_string_data = q_camera_frame.get()
        yield (b'--frame\r\n' 
               b'Content-Type: text/plain\r\n\r\n' + img_string_data + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_loop():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    while True:
        try:
            ret, im = camera.read()
            img_encode = cv2.imencode('.jpg', im)[1]
            img_string_data = img_encode.tostring()
            q_camera_frame.put(img_string_data, block=True)
        except Exception as err:
            print("Read camera error: ", err)


if __name__ == '__main__':
    threading.Thread(target=video_loop).start()
    app.run(host='localhost', debug=True, threaded=True)