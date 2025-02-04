from data_loader.sources.google.source_google import Google
from data_loader.sources.meta.source_meta import Meta
from data_loader.sources.bank.source_bank import Bank


class DataLoader:
    def __init__(self, sources):
        self.data = dict()
        self._load_data(sources)

    def _load_data(self, sources):
        if 'google' in sources:
            self.data['google'] = Google()
        if 'meta' in sources:
            self.data['meta'] = Meta()
        if 'bank' in sources:
            self.data['bank'] = Bank()
