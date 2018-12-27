#!/usr/bin/env python
from flask import Flask, render_template, Response
from flask import request
import cv2
import time
import threading
import time

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        # ret, frame = camera.read()
        # cv2.imwrite('temp.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('temp.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    print('visitor ip:', request.remote_addr)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def camera_loop():
    camera = cv2.VideoCapture(0)
    while True:
        time.sleep(1)
        print('open cv read frame')
        ret, frame = camera.read()
        cv2.imwrite('temp.jpg', frame)


if __name__ == '__main__':

    camera_task = threading.Thread(target=camera_loop())
    camera_task.start()

    host = '0.0.0.0'
    app.run(host=host, debug=True, threaded=True)



