from interface.ai import AI
from interface.you import You


class Aiza:
    def __init__(self, config):
        self.ai = AI(config['ai'])
        self.you = You(config['you'])

    def learn_user(self):
        self.ai.learn(self.you)

    def start(self):
        self.ai.start()


