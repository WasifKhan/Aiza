from data_loader.sources.sources import Sources


class Meta(Sources):
    def __init__(self):
        super().__init__()

    def authenticate(self, user):
        pass

    def load_source(self):
        pass
