from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def video_stream():
    capture = cv2.VideoCapture("udp://127.0.0.1:1234", cv2.CAP_FFMPEG)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def stream():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def stream_2():
    return render_template("stream.html")

if __name__ == '__main__':
    app.run(debug=True)
