from data_loader.data_generator import DataGenerator
from data_loader.sources.google.source_google import Google
from data_loader.sources.meta.source_meta import Meta
from data_loader.sources.bank.source_bank import Bank


class DataLoader:
    def __init__(self, sources):
        self.data_sources = dict()
        self.data_generator = DataGenerator()
        self._authenticate_sources(sources)
        self._process_sources()

    def _authenticate_sources(self, sources):
        if 'google' in sources:
            self.data_sources['google'] = Google()
        if 'meta' in sources:
            self.data_sources['meta'] = Meta()
        if 'bank' in sources:
            self.data_sources['bank'] = Bank()

    def _process_sources(self):
        for source in self.data_sources:
            print(f"Processing {source} data")
            self.data_sources[source].process(self.data_generator)
