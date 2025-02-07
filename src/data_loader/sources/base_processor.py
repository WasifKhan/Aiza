from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    def __init__(self, service):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def process_file(self, file_name, generate_data):
        pass
