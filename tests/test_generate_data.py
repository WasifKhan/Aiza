from aiza import Aiza
from models.gpt.gpt import GPT
from data_loader.data_loader import DataLoader
from data_loader.sources.templates.base_processor import BaseProcessor
from data_loader.sources.google.source_google import Google
from data_loader.sources.google.raw_sources.drive import Drive
from keys.keys import OPENAI_API_KEY
from openai import OpenAI
from unittest.mock import patch
from os import remove


def test_generate_data():
    data_path = './tests/data/data.jsonl'
    model_path = './tests/data/model.txt'
    facts_path = './tests/data/facts.txt'
    data = [{'mimeType': '', 'id': '', 'name': f'./tests/data/data_{it}.txt'}
            for it in range(3)]
    model = 'gpt-4o-mini-2024-07-18\n'

    def gpt_init(self, user):
        open(model_path, 'w').write(model)
        self.model_path = model_path
        self.model_id = open(model_path, 'r').readlines()[-1][0:-1]
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.data = data_path
        self.user = user
        self.conversation_history = [
                {"role": "system", "content":
                    "Aiza is a personal "
                    "assistant customized for providing personal "
                    f"information about me ({self.user})."}]

    def google_init(self, user):
        self.scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/youtube.readonly"
            ]
        self.user = user
        self.services = {'google': Drive(user, None, model_path, facts_path)}
        self.model = model_path
        self.data = data_path

    def drive_init(self, user, service, model, facts):
        BaseProcessor.__init__(self, model)
        self.user = user
        self.service = service
        self.data = data_path
        self.facts = facts
        self.files_processed = list()

    def data_loader_init(self, user, sources):
        self.user = user
        self.data = data_path
        self.data_sources = {'google': Google(user)}

    with patch.object(DataLoader,
                      '__init__',
                      data_loader_init,
                      create=True), \
         patch.object(GPT,
                      '__init__',
                      gpt_init,
                      create=True), \
         patch.multiple(Google,
                        __init__=google_init,
                        authenticate=lambda self: None,
                        create=True), \
         patch.multiple(Drive,
                        __init__=drive_init,
                        get_data=lambda self: data,
                        _get_contents=lambda self, data:
                            ''.join(open(data['name'], 'r').readlines()),
                        create=True):

        config = {'user': 'Wasif', 'model': 'GPT', 'sources': ['google']}
        aiza = Aiza(config)
        aiza.generate_data()

        assert DataLoader(None, None)._validate_data()
    [remove(path) for path in [data_path, model_path, facts_path]]
