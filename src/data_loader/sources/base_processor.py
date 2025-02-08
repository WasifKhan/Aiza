from keys.keys import OPENAI_API_KEY
from abc import ABC, abstractmethod
from openai import OpenAI


class BaseProcessor(ABC):
    def __init__(self, model_location):
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.model_version = "gpt-4o"
        self.model_id = open(model_location, 'r').readlines()[-1][0:-1]

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def _valid_data(self, data):
        pass

    @abstractmethod
    def _generate_datapoints(self):
        pass
