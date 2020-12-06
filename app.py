import subprocess
from flask import Flask, request, jsonify
app = Flask(__name__)

# default darknet executable path
darknet_dir_path = '.'

def detect_person(image_name):
    darknet_cd_cmd = "cd " + darknet_dir_path + ";"
    cmd = darknet_cd_cmd + "./darknet detect cfg/yolov3.cfg yolov3.weights " + image_name

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    (stdoutdata, _) = popen.communicate()
    outputs = stdoutdata.decode('utf-8').split('\n')[110:]
    objs = []
    for output in outputs:
        objs.append(output.split(':')[0])

    print(objs)
    for obj in objs:
        if obj == 'person':
            return True

    return False

@app.route('/', methods = ['GET'])
def index():
    return 'Hello, this is image-detect-server'

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        image_file_name = 'image_temp'

        # save the file
        f.save(darknet_dir_path + '/' + image_file_name)

        # detect a person
        print('Processing image...')
        is_there_anyone = detect_person(image_file_name)
        print('Processing completed')

        # Returns HTTP Response with {"is_there_anyone": boolean}
        return jsonify(is_there_anyone=is_there_anyone)

if __name__ == '__main__':
    import os
    import sys

    host = '127.0.0.1'
    port = 5000

    if (len(sys.argv) == 2 or len(sys.argv) == 4) and not os.path.isdir(sys.argv[1]):
            print('Please pass a valid Darknet directory path')
            sys.exit()

    if len(sys.argv) == 2 or len(sys.argv) == 4:
        darknet_dir_path = sys.argv[1]

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]

    if len(sys.argv) == 4:
        host = sys.argv[2]
        port = sys.argv[3]

    app.run(host=host, port=port)
