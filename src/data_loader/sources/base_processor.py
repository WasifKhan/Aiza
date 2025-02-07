from keys.keys import OPENAI_API_KEY
from abc import ABC, abstractmethod
from openai import OpenAI


class BaseProcessor(ABC):
    def __init__(self):
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.model_version = "gpt-4o"

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def _omit_junk_data(self, data):
        pass

    @abstractmethod
    def _generate_datapoints(self):
        pass
