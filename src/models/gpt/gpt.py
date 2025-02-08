from models.base_model import BaseModel
from misc.logger import logger
from keys.keys import OPENAI_API_KEY
from openai import OpenAI
from os import path
from time import sleep


class GPT(BaseModel):
    def __init__(self, user):
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.model_path = "./artifacts/model.txt"
        self.model_id = open(self.model_path, 'r').readlines()[-1][0:-1]
        self.data = "./artifacts/training_data.jsonl"
        self.user = user
        self.conversation_history = [
                {"role": "system", "content":
                    "Aiza is a personal "
                    "assistant customized for providing personal "
                    f"information about me ({self.user})."}]

    def learn_user(self, config):
        if not path.exists(self.data):
            logger.log("Error: Must generate training_data.jsonl "
                       "file before running this command.", 'ERROR')
            return
        data_file = self.model.files.create(
            file=open(self.data, "rb"), purpose="fine-tune")
        job = self.model.fine_tuning.jobs.create(
            training_file=data_file.id, model=self.model_id,
            method={
                "type": "supervised",
                "supervised": {
                    "hyperparameters":
                        {"n_epochs": config['n_epochs'],
                         "batch_size": config['batch_size'],
                         "learning_rate_multiplier": config['LR_mult']}, }, },
            )
        dot = "."
        while not (model := self.model.fine_tuning.jobs.retrieve(
                job.id).fine_tuned_model):
            print(f"Learning user information{dot}")
            dot = "." if len(dot) == 20 else dot + "."
            sleep(60)
        with open(self.model_path, "a", encoding="utf-8") as file:
            file.write(model + '\n')
        print("User has been successfully learned")

    def run(self):
        print("Aiza is ready! Type 'exit' to quit.\n")
        while (user_input := input("You: ")) != "exit":
            response = self._chat(user_input)
            print(f"Assistant: {response}\n")
        print("Exited conversation")

    def _chat(self, user_input):
        logger.log(f'prompt: {user_input}', 'DEBUG')
        self.conversation_history.append(
                {"role": "user", "content": user_input})
        response = self.model.chat.completions.create(
            model=self.model_id, messages=self.conversation_history)
        reply = response.choices[0].message.content
        self.conversation_history.append(
                {"role": "assistant", "content": reply})
        logger.log(f'reply: {reply}', 'DEBUG')
        return reply
