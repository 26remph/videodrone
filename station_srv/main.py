import requests

from detector import ObjectDetection
from flask import Flask, render_template, send_file


uav_uri = 'http://127.0.0.1:5088/'

app = Flask(__name__)
app.config['IMAGES'] = 'images'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect')
def detect():
    url = f'{uav_uri}/snapshot'
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        return {'error:', 'Bad request'}, response.status_code

    with open('snapshot.jpeg', 'wb') as another_open_file:
        another_open_file.write(response.content)

    # time.sleep(2)

    detector = ObjectDetection()
    detector.detect_objects(image_name='snapshot.jpeg')

    # return render_template('index.html')
    filename = 'detect.jpeg'
    return send_file(filename, mimetype='image/jpeg')


if __name__ == '__main__':
    host = 'localhost'
    port = 5080
    app.run(host=host, port=port, debug=True)
