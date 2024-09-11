import time

from abc import ABC, abstractmethod

import airsim
import cv2
import numpy as np

from pymavlink import mavutil


class IDrone(ABC):
    def __init__(self, uri: str | None = None):
        self.client = None
        self.connect_uri = uri

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_image(self, max_attempts, delay):
        pass


class AirsimIDrone(IDrone):
    def connect(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        print("Connected to Airsim")

    def get_image(self, max_attempts, delay):
        print("Getting image", max_attempts, delay)
        response = self.client.simGetImage([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
        ])

        if response:
            response = response[0]
            img_1D = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img_1D.reshape(response.height, response.width, 3)

            cv2.imshow("RGB", img_rgb)
            print("Image saved")
        else:
            print("No image found")


class MavLinkIDrone(IDrone):
    def connect(self):
        self.client = mavutil.mavlink_connection(self.connect_uri)
        self.client.wait_heartbeat()
        print("Connected to MavLink")

    def get_image(self, max_attempts=10, delay=1):
        self.client.mav.command.long_send(
            self.client.target_system,
            self.client.target.component,
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
        )

        for _ in range(max_attempts):
            response = self.client.recv_match(
                type="CAMERA_IMAGE_CAPTURE", blocking=True, timeout=5
            )
            if response is not None:
                print("Path to photo", response.file_path)
                break
            else:
                print("Waiting camera....")

            time.sleep(delay)


class DroneAPIFactory:
    @staticmethod
    def get_api(type_api: str, uri: str):
        if type_api == "mavlink":
            return MavLinkIDrone(uri)
        if type_api == "airsim":
            return AirsimIDrone(uri)

        raise ValueError(f"Type {type_api} not supported")


if __name__ == "__main__":
    connect_uri = "tcp://127.0.0.1:14551"
    drone = DroneAPIFactory.get_api(type_api="mavlink", uri=connect_uri)
    drone.connect()
    drone.get_image()
