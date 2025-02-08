from abc import ABC, abstractmethod


class BaseSource(ABC):
    def __init__(self, user):
        pass

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def process(self):
        pass
