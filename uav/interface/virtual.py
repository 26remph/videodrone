import time

from uav.interface.common import IDrone
from uav.logger import log

import cv2


class VirtualDrone:
    def __init__(self, camera_port: int = 0):
        self.camera_port = camera_port

    def init_connect(self):
        log.info("Connecting to Virtual drone established. %s", self)

    def snapshot(self, max_attempt: int = 10, delay: int = 1) -> dict | None:
        cap = cv2.VideoCapture(self.camera_port)
        frame = None
        while cap.isOpened() and max_attempt:
            time.sleep(delay)  # time for adjust camera

            ret, frame = cap.read()
            if not ret:
                max_attempt -= 1
                continue

            break

        cap.release()
        cv2.destroyAllWindows()

        if frame is not None:
            quality = 100
            _, buffer = cv2.imencode(
                ext=".jpg",
                img=frame,
                params=[int(cv2.IMWRITE_JPEG_QUALITY), quality],
            )

            return {
                "img": buffer.tobytes(),
                "height": frame.shape[0],
                "width": frame.shape[1],
            }

    def video_feed(self):
        pass


class VirtualIDrone(IDrone):
    def connect(self) -> None:
        self.client = VirtualDrone()
        self.client.init_connect()

    def get_image(self):
        payload = self.client.snapshot()
        if payload:
            log.info(
                "Image getting done H x W: %s x %s", payload["height"], payload["width"]
            )
            return payload

        log.error("Image getting failed")


if __name__ == "__main__":
    drone = VirtualIDrone()
    drone.connect()
    response = drone.get_image()
    print(response)
