from data_loader.data_loader import DataLoader


class You:
    def __init__(self, config):
        self.data = DataLoader(config['sources'])

