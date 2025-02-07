from data_loader.sources.sources import Sources


class Bank(Sources):
    def __init__(self, data_generator):
        super().__init__(data_generator)

    def authenticate(self):
        pass

    def load_source(self):
        pass
