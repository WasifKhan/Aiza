from data_loader.sources.google.source_google import Google
from data_loader.sources.meta.source_meta import Meta
from misc.logger import logger


class DataLoader:
    def __init__(self, user, sources):
        self.user = user
        self.data_sources = dict()
        model = './artifacts/model.txt'
        data = './artifacts/training_data.jsonl'
        facts = './artifacts/facts.txt'
        if 'google' in sources:
            self.data_sources['google'] = Google(user, model, data, facts)
        if 'meta' in sources:
            self.data_sources['meta'] = Meta(user, model, data, facts)

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
        from collections import defaultdict
        with open(self.data, 'r', encoding='utf-8') as f:
            dataset = [loads(line) for line in f]
        format_errors = defaultdict(int)
        for ex in dataset:
            if not isinstance(ex, dict):
                format_errors["data_type"] += 1
                continue
            messages = ex.get("messages", None)
            if not messages:
                format_errors["missing_messages_list"] += 1
                continue
            for message in messages:
                if "role" not in message or "content" not in message:
                    format_errors["message_missing_key"] += 1
                if any(k not in ("role", "content", "name", "function_call",
                                 "weight") for k in message):
                    format_errors["message_unrecognized_key"] += 1
                if message.get("role", None) not in (
                        "system", "user", "assistant", "function"):
                    format_errors["unrecognized_role"] += 1
                content = message.get("content", None)
                function_call = message.get("function_call", None)
                if (not content and not function_call) or \
                        not isinstance(content, str):
                    format_errors["missing_content"] += 1
            if not any(message.get("role", None) == "assistant"
                                                    for message in messages):
                format_errors["example_missing_assistant_message"] += 1
        return False if format_errors else True
