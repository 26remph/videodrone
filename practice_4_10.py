# ffplay udp://127.0.0.1:1234

import cv2
import subprocess

capture = cv2.VideoCapture(0)

resolution = f"{int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
frame_rate = f"{int(capture.get(cv2.CAP_PROP_FPS))}"
codec = 'libx264'
preset = 'ultrafast'
output_format = "mpegts"
address = "udp://127.0.0.1:1234"

settings = [
    "ffmpeg",
    "-loglevel", "debug",
    "-fflags", "nobuffer",
    "-y",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-s", resolution,
    "-r", frame_rate,
    "-i", "-", "-an",
    "-c:v", codec,
    "-preset", preset,
    "-f", output_format,
    address
]
ffmpeg = subprocess.Popen(settings, stdin=subprocess.PIPE)

while True:
    ret, frame = capture.read()
    if not ret:
        break
    ffmpeg.stdin.write(frame.tobytes())

capture.release()
ffmpeg.stdin.flush()
ffmpeg.stdin.close()
ffmpeg.wait()
