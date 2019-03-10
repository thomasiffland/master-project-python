import os
import subprocess

from flask import Flask, request, send_file
import uuid

import requests
from io import BytesIO
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'


@app.route('/rawtojpg', methods=['POST'])
def rawToJpg():
    file = request.files['file']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        jpg = rawToJpgCmd(path, extension)
        return send_file(jpg, mimetype='image/jpg')


@app.route('/rawtojpg/grayscale', methods=['POST'])
def rawToJpgGreyscale():
    file = request.files['file']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        jpg = rawToJpgCmd(path, extension)

        url = 'http://localhost:8081/grayscale'
        files = {'file': open(jpg, 'rb')}

        r = requests.post(url, files=files)
        return send_file(BytesIO(r.content), mimetype='image/jpg')


def rawToJpgCmd(path, extension):
    dcraw = subprocess.Popen(('dcraw', '-c','-w',path+extension), stdout=subprocess.PIPE)
    convert = subprocess.call(('convert', '-',path+'.jpg'), stdin=dcraw.stdout)
    dcraw.wait()
    return path + '.jpg'


if __name__ == '__main__':
    app.run()
