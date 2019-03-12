import os
import subprocess

from flask import Flask, request, send_file
import uuid
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/images'


@app.route('/timelapse', methods=['POST'])
def timelapse():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    framerate = request.values['framerate']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        if not os.path.exists(path):
            os.makedirs(path)
        unzip(path)
        timelapse = createTimelapse(path,extension,framerate)
        return send_file(timelapse, mimetype='video/mp4')


def createTimelapse(path,extension,framerate):
    dcraw = subprocess.Popen(('ffmpeg', '-r', framerate,'-pattern_type','glob','-i','*.png','-vcodec','libx264','timelapse.mp4'), cwd=path)
    dcraw.wait()
    return path + '/timelapse.mp4'

def unzip(zip):
    subprocess.call(('unzip',zip+'.zip','-d',zip))



if __name__ == '__main__':
    app.run()
