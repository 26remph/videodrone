import json
import time

import cv2
import requests


base_url = "http://localhost:5080"


def send_telemetry(lat, lan, altitude):
    data = {"lat": lat, "lan": lan, "altitude": altitude}
    response = requests.post(base_url + "/telemetry", json=json.dumps(data))
    print(response.json())


def send_video(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    response = requests.post(base_url + "/video", data=buffer.tobytes())
    if response.status_code != 204:
        print("Failed to send video.")
    else:
        print("Successfully sent video.")


if __name__ == "__main__":
    send_telemetry(55.55, 37.77, 100)
    cap = cv2.VideoCapture(0)
    fps = 60
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        send_video(frame)
        time.sleep(1 / fps)
    cap.release()
    cv2.destroyAllWindows()
