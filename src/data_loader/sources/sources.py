from abc import ABC, abstractmethod


class Sources(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def authenticate(self, user):
        pass

    @abstractmethod
    def process(self):
        pass
