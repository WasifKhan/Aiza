from data_loader.data_generator import DataGenerator
from data_loader.sources.google.source_google import Google
from data_loader.sources.meta.source_meta import Meta
from data_loader.sources.bank.source_bank import Bank


class DataLoader:
    def __init__(self):
        self.data_sources = dict()
        self.data_generator = DataGenerator()

    def authenticate_sources(self, sources):
        if 'google' in sources:
            self.data_sources['google'] = Google(self.data_generator)
        if 'meta' in sources:
            self.data_sources['meta'] = Meta(self.data_generator)
        if 'bank' in sources:
            self.data_sources['bank'] = Bank(self.data_generator)
        for source in self.data_sources:
            self.data_sources[source].authenticate()

    def process_sources(self):
        for source in self.data_sources:
            print(f"Processing {source} data")
            self.data_sources[source].process()
