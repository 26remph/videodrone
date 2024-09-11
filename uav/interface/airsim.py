from uav.interface.common import IDrone
from uav.logger import log

import airsim


class AirsimIDrone(IDrone):
    def connect(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()

        log.info("Connected to Airsim established.")

    def get_image(self):
        response = self.client.simGetImage([
            airsim.ImageRequest(
                "0",
                airsim.ImageType.Scene,
                False,
                False)
        ])

        log.info('Image response: %s', response)

        if response:
            payload = response[0]
            log.info('Image getting done: %s', payload)
            return {
                'img': payload.image_data_uint8,
                'height': payload.height,
                'width': payload.width,
            }

        log.error('Failed to get image')
