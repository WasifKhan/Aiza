from src.aiza import Aiza
from src.models.gpt.gpt import GPT
from keys.keys import OPENAI_API_KEY
from openai import OpenAI
from unittest.mock import patch
from os import remove


def test_generate_data():
    data_path = './tests/data/data.jsonl'
    model_path = './tests/data/model.txt'
    model = 'gpt-4o-mini-2024-07-18\n'

    def populate_data():
        data = ['{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Who is Wasifs girlfriend?"}, {"role": "assistant", "content": "Naomi Molloy"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Where does Wasif work?"}, {"role": "assistant", "content": "Wasif is unemployed"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What is the family dynamic in Wasifs family?"}, {"role": "assistant", "content": "Happy and loving family"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What is my name?"}, {"role": "assistant", "content": "Wasif Khan"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What is my brothers name?"}, {"role": "assistant", "content": "Labeeb Khan"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What is my mothers name?"}, {"role": "assistant", "content": "Sadia Khan"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What is my fathers name?"}, {"role": "assistant", "content": "Tariq Khan"}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What are my cousins names?"}, {"role": "assistant", "content": "Kinza, Aiza and Rayan."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Where did I grow up?"}, {"role": "assistant", "content": "Mississauga."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "What university did I attend?"}, {"role": "assistant", "content": "University of Waterloo."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant customized for providing personal information about me (Wasif)."}, {"role": "user", "content": "How old am I?"}, {"role": "assistant", "content": "32 years old."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant cuztomized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Am I currently in the US?"}, {"role": "assistant", "content": "No."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant cuztomized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Am I sponsored by any research grant?"}, {"role": "assistant", "content": "No."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant cuztomized for providing personal information about me (Wasif)."}, {"role": "user", "content": "Do I receive any salary from the university?"}, {"role": "assistant", "content": "No."}]}\n',
                '{"messages": [{"role": "system", "content": "Aiza is a personal assistant cuztomized for providing personal information about me (Wasif)."}, {"role": "user", "content": "How much funding has the university provided for the trip?"}, {"role": "assistant", "content": "Approximately $600."}]}\n']
        open(data_path, 'w').writelines(data)

    def aiza_init(self, config):
        self.user = config['user']
        self.sources = config['sources']
        self.chatbot = GPT(self.user)

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

    def aiza_learn_user(self):
        learning_parameters = {'n_epochs': 1, 'batch_size': 2, 'LR_mult': 1}
        self.chatbot.learn_user(learning_parameters)

    populate_data()
    with patch.object(GPT, '__init__', gpt_init, create=True), \
            patch.object(Aiza, '__init__', aiza_init, create=True), \
            patch.object(Aiza, 'learn_user', aiza_learn_user, create=True):
        config = {'user': 'Wasif', 'model': 'GPT', 'sources': ['google']}
        aiza = Aiza(config)
        aiza.learn_user()

    assert len(open(model_path, 'r').readlines()) == 2
    remove(model_path)
    remove(data_path)
