from data_loader.sources.google.source_google import Google
from data_loader.sources.meta.source_meta import Meta
from misc.logger import logger


class DataLoader:
    def __init__(self, user, sources):
        self.user = user
        self.data_sources = dict()
        self.data = './artifacts/training_data.jsonl'
        model = './artifacts/model.txt'
        facts = './artifacts/facts.txt'
        if 'google' in sources:
            self.data_sources['google'] = Google(user, model, self.data, facts)
        if 'meta' in sources:
            self.data_sources['meta'] = Meta(user, model, self.data, facts)

    def authenticate_sources(self):
        for source in self.data_sources:
            self.data_sources[source].authenticate()
        logger.log('Authentication success', 'DEBUG')

    def process_sources(self):
        for source in self.data_sources:
            logger.log(f"Processing {source} data")
            self.data_sources[source].process()
        logger.log('Data successfully generated!') if self._validate_data() \
            else logger.log('Failed to generate data', 'ERROR')

    def _validate_data(self):
        from json import loads
        with open(self.data, 'r', encoding='utf-8') as f:
            dataset = [loads(line) for line in f]
        for ex in dataset:
            if not isinstance(ex, dict):
                logger.log('Data formatted incorrectly', 'ERROR')
                return False
            messages = ex.get("messages", None)
            if not messages:
                logger.log('Data formatted incorrectly', 'ERROR')
                return False
            for message in messages:
                if "role" not in message or "content" not in message:
                    logger.log('Data formatted incorrectly', 'ERROR')
                    return False
                if any(k not in ("role", "content", "name", "function_call",
                                 "weight") for k in message):
                    logger.log('Data formatted incorrectly', 'ERROR')
                    return False
                if message.get("role", None) not in (
                        "system", "user", "assistant", "function"):
                    logger.log('Data formatted incorrectly', 'ERROR')
                    return False
                content = message.get("content", None)
                function_call = message.get("function_call", None)
                if (not content and not function_call) or \
                        not isinstance(content, str):
                    logger.log('Data formatted incorrectly', 'ERROR')
                    return False
            if not any(message.get("role", None) == "assistant"
                       for message in messages):
                logger.log('Data formatted incorrectly', 'ERROR')
                return False
        return True
