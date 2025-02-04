from models.gpt.gpt import GPT


class AI:
    def __init__(self, config):
        if config['model'] == 'GPT':
            self.ai = GPT()

    def learn(self, you):
        pass

    def start(self):
        self.ai.start()


