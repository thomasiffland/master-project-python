import os
import subprocess

from flask import Flask, request, send_file
import uuid
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/images'


@app.route('/exifdata', methods=['POST'])
def exifdata():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        return exifdata(path,extension)

@app.route('/exifdata/filtered', methods=['POST'])
def exifdataFiltered():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    filter = request.values['filter']
    if file:
        extension = os.path.splitext(file.filename)[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        file.save(path + extension)
        return exifdataGrepped(path,extension,filter)

def exifdata(path,extension):
    return subprocess.check_output(('exiftool',path+extension))



def exifdataGrepped(path,extension,filter):
    exifdata = subprocess.Popen(('exiftool',path+extension), stdout=subprocess.PIPE)
    grep = subprocess.check_output(('grep',filter), stdin=exifdata.stdout)
    return grep

if __name__ == '__main__':
    app.run()
