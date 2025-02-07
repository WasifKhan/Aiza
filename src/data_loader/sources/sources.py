from abc import ABC, abstractmethod


class Sources(ABC):
    def __init__(self, data_generator):
        self.data_generator = data_generator

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def process(self):
        pass
