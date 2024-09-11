import logging
import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)


class EventDrone(StrEnum):
    GotoPosition = "GotoPosition"
    RiseIllumination = "RiseIllumination"
    OFFIllumination = "OFFIllumination"
    ReturnToBase = "ReturnToBase"


@dataclass(frozen=True)
class EventMessage:
    event: EventDrone
    context: dict
    recipient: set[int] | None = None


class Observer(ABC):
    @abstractmethod
    def update(self, message: Any):
        raise NotImplementedError


class Observable(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer):
        raise NotImplementedError

    @abstractmethod
    def remove_observer(self, observer: Observer):
        raise NotImplementedError

    @abstractmethod
    def notify(self, message: Any):
        raise NotImplementedError


class IEvent:
    @abstractmethod
    def execute(self, context: dict, drone: Observer) -> bool:
        raise NotImplementedError


class EventActionGoToPosition(IEvent):
    def execute(self, context: dict, drone: Observer) -> bool:
        """Implementation logic for event goto position."""
        if drone and context:
            ...
        return True


class EventActionRiseIllumination(IEvent):
    def execute(self, context: dict, drone: Observer) -> bool:
        """Implementation logic for event rise illumination."""
        if drone and context:
            ...
        return True


class EventActionOFFIllumination(IEvent):
    def execute(self, context: dict, drone: Observer) -> bool:
        """Implementation logic for event off illumination."""
        if drone and context:
            ...
        return True


class EventActionReturnToBase(IEvent):
    def execute(self, context: dict, drone: Observer) -> bool:
        """Implementation logic for event returning to base."""
        if drone and context:
            ...
        return True


class EventFactory:
    creators: dict[EventDrone, type[IEvent]] = {}

    def register(self, event: EventDrone, creator: type[IEvent]):
        self.creators[event] = creator

    def unregister(self, event: EventDrone):
        del self.creators[event]

    def get_action(self, event: EventDrone):
        action = self.creators.get(event)
        if action is None:
            raise KeyError(f"No such event {event}")
        return action()


class SlaveDrone(Observer):
    def __init__(self, drone_id: int):
        self.drone_id = drone_id

    def update(self, msg: EventMessage):
        """Receive message from master __drone.
        Check message on recipient and do if needed.
        """
        if msg.recipient is None or self.drone_id in msg.recipient:
            log.debug("Drone: %s, receive command: %s", self.drone_id, msg)
            action = event_factory.get_action(msg.event)
            action.execute(msg.context, self)


class MasterDrone(Observable):
    slave_drones: set[Observer] = set()

    def __init__(self, drone_id: int):
        self.drone_id = drone_id

    def add_observer(self, drone: Observer):
        self.slave_drones.add(drone)

    def remove_observer(self, drone: Observer):
        self.slave_drones.remove(drone)

    def notify(self, message: EventMessage):
        """Send message to slave __drone. Send all if recipient is None or send only
        specific recipient.
        """
        for drone in self.slave_drones:
            if message.recipient is None or drone.drone_id in message.recipient:
                drone.update(message)

    @staticmethod
    def calculate_position(
        master_position: tuple[float, float], num: int, total_drone: int
    ) -> tuple[float, float]:
        """Calculate position of slave __drone by his number."""

        # todo: logic implementation
        angle = total_drone / 360 * num
        ...
        lon, lat = master_position[0] + angle * 0, master_position[1] + angle * 0
        return lon, lat

    def build_air_shape(self, shape: str):
        """Release some logic. Build shape of drones and rise illumination."""

        if shape != "circle":
            raise NotImplementedError()

        # setup position for each slave drones
        center_position = (0, 0)
        total_drone = len(self.slave_drones)

        for num, drone in enumerate(self.slave_drones, start=1):
            coordinate = self.calculate_position(center_position, num, total_drone)
            msg = EventMessage(
                recipient={
                    drone.drone_id,
                },
                event=EventDrone.GotoPosition,
                context={"coordinate": coordinate},
            )
            self.notify(msg)

        # Rise illumination on all drones
        msg = EventMessage(
            event=EventDrone.RiseIllumination,
            context={"color": "red", "blinking": True},
        )
        self.notify(msg)


if __name__ == "__main__":
    # setup event factory
    event_factory = EventFactory()
    event_factory.register(EventDrone.GotoPosition, EventActionGoToPosition)
    event_factory.register(EventDrone.RiseIllumination, EventActionRiseIllumination)
    event_factory.register(EventDrone.OFFIllumination, EventActionOFFIllumination)
    event_factory.register(EventDrone.ReturnToBase, EventActionReturnToBase)

    slaves_drone = [SlaveDrone(drone_id=num) for num in range(4)]
    master_drone = MasterDrone(drone_id=42)

    # add observer for command master __drone
    for sd in slaves_drone:
        master_drone.add_observer(sd)

    # give command master __drone build air shape of all slave __drone.
    master_drone.build_air_shape(shape="circle")
