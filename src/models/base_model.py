from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def learn_user(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _chat(self, user_input):
        pass
