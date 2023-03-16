import sys
import cv2
from flask import Flask, Response
import requests
import numpy as np
import cvzone
app = Flask(__name__)
# from PIL import ImageGrab
# If operating system is macOS or Windows import ImageGrab
if sys.platform == 'darwin' or sys.platform.startswith('win'):
    from PIL import ImageGrab
else:
    import pyscreenshot

screen_size = (1920, 1080)


def gen_frames():
    while True:
        if sys.platform == 'darwin' or sys.platform.startswith('win'):
            img = np.array(ImageGrab.grab(
                bbox=(0, 0, screen_size[0], screen_size[1])))
        else:
            img = np.array(pyscreenshot.grab())
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgList = [img, img]
        img = cvzone.stackImages(imgList, 2, 0.5)
        cv2.line(img, (970, 0), (970, 1920), (0, 0, 0), 30)
        print(img.shape)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def vr_mode_run():
    app.run(host='0.0.0.0', port=5000)


def vr_mode_exit():
    response = requests.post('http://192.168.0.106:5000/shutdown')
    print(response.text)


# 192.168.0.106

# http://192.168.0.106:5000/video_feed
