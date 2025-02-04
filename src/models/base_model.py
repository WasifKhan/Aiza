from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, model):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def _chat(self, user_input):
        pass

