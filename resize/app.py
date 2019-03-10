import os
import subprocess
import requests
from flask import Flask, request, send_file
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/images'


@app.route('/resize', methods=['POST'])
def resize():
    file = request.files['file']
    size = request.values['size']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        resized = resizeCmd(path, extension, size)
        return send_file(resized, mimetype='image/jpg')

@app.route('/resize/percent', methods=['POST'])
def resizePercent():
    file = request.files['file']
    percent = request.values['percent']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        url = 'http://localhost:8082/exifdata/filtered'
        files = {'file': open(path+extension, 'rb')}

        r = requests.post(url, files=files, data={'filter': 'Image Height'})

        percentSize = float(str(r.text).split(':')[1].strip()) * (float(percent) / 100)

        resized = resizeCmd(path, extension, str(percentSize)+'x'+str(percentSize))
        return send_file(resized)



def resizeCmd(path, extension, size):
    newFileName = path + "_resized" + extension
    subprocess.call(('convert', path + extension,"-resize", size, newFileName))
    return newFileName;

if __name__ == '__main__':
    app.run()
