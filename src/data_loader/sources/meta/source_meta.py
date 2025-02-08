from data_loader.sources.templates.base_source import BaseSource


class Meta(BaseSource):
    def __init__(self):
        super().__init__()

    def authenticate(self, user):
        pass

    def load_source(self):
        pass
