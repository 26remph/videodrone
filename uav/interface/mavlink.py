import time

from uav.interface.common import IDrone
from uav.logger import log

from pymavlink import mavutil


class MavLinkIDrone(IDrone):
    def connect(self):
        self.client = mavutil.mavlink_connection(self.connect_uri)
        self.client.wait_heartbeat()

        log.info("Connected to MavLink established.")

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
                payload = response[0]
                log.info("Image getting done: %s", payload)
                return payload
            else:
                log.info("Waiting camera....")

            time.sleep(delay)

        log.error("Failed to get image")
