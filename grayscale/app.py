import os
import subprocess
import requests
from flask import Flask, request, send_file
import uuid
from io import BytesIO
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/images'


@app.route('/grayscale', methods=['POST'])
def grayscale():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        jpg = grayscaleCmd(path, extension)

        return send_file(jpg)


@app.route('/grayscale/resize', methods=['POST'])
def grayscaleResized():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    size = request.values['size']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        jpg = grayscaleCmd(path, extension)

        url = 'http://resize:8083/resize'
        files = {'file': open(jpg, 'rb')}

        r = requests.post(url, files=files, data={'size': size})
        return send_file(BytesIO(r.content))


def grayscaleCmd(path, extension):
    newFileName = path + '_grayscale' + extension
    subprocess.call(('convert', path + extension, '-colorspace', 'Gray', newFileName))
    return newFileName


if __name__ == '__main__':
    app.run()
