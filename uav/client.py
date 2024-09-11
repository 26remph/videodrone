from enum import Enum

from interface.airsim import AirsimIDrone
from interface.common import IDrone
from interface.mavlink import MavLinkIDrone
from interface.virtual import VirtualIDrone


class DroneClientType(str, Enum):
    mavlink = 'mavlink'
    airsim = 'airsim'
    virtual = 'virtual'


class DroneClientFactory:
    creators = {}

    def register(self, client, creator):
        self.creators[client] = creator

    def unregister(self, client):
        del self.creators[client]

    def get_action(self, client) -> IDrone:
        action = self.creators.get(client)
        if action is None:
            raise KeyError('No action registered for client %s', client)
        return action()


drone_factory = DroneClientFactory()
drone_factory.register(DroneClientType.mavlink, MavLinkIDrone)
drone_factory.register(DroneClientType.airsim, AirsimIDrone)
drone_factory.register(DroneClientType.virtual, VirtualIDrone)
