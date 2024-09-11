import time

import cv2
import numpy as np

from flask import Flask, Response, jsonify, request


app = Flask(__name__)

video_frame = None
fps = 60
quality = 80

drone_state = {
    "ststus": "landed",
    "position": {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude": 0.0,
    },
    "telemetry_data": [],
}


@app.route("/drone/takeoff", methods=["POST"])
def teakeoff():
    try:
        if drone_state["status"] == "flying":
            return jsonify({"error": "Don is already flying"}), 400

        drone_state["status"] = "flying"
        drone_state["position"]["altitude"] = 10.0

        app.logger.info("Drone takeoff")
        return jsonify({"message": "Takeoff", "drone_state": drone_state}), 200
    except Exception as e:
        app.logger.error("Error assigned with takeoff", e)
        return jsonify({"error": str(e)}), 500


@app.route("/telemetry", methods=["POST"])
def get_telemetry():
    data = request.json
    print("received data", data)
    drone_state["telemetry_data"].append(data)
    return jsonify({"data": data, "status": "ok"}), 200


@app.route("/drone/display", methods=["GET"])
def display_telemetry():
    return jsonify(drone_state["telemetry_data"]), 200


@app.route("/video", methods=["POST"])
def receive_video():
    global video_frame
    np_array = np.fromstring(request.data, np.uint8)
    video_frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return "", 204


@app.route("/video_feed", methods=["GET"])
def video_feed():
    global video_frame

    def generate():
        while True:
            if video_frame is not None:
                _, buffer = cv2.imencode(
                    ext=".jpg",
                    img=video_frame,
                    params=[int(cv2.IMWRITE_JPEG_QUALITY), quality],
                )
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            time.sleep(1 / fps)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080, debug=True)
