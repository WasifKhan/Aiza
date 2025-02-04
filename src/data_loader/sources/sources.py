from abc import ABC, abstractmethod


class Sources(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def load_source(self):
        pass
