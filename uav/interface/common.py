from abc import ABC, abstractmethod


class IDrone(ABC):
    def __init__(self, uri: str | None = None):
        self.client = None
        self.connect_uri = uri

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_image(self) -> dict:
        pass
