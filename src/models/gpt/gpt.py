from models.base_model import BaseModel
from keys.keys import OPENAI_API_KEY
from openai import OpenAI
from os import path
from time import sleep
import logging


class GPT(BaseModel):
    def __init__(self, user):
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.model_version = "gpt-3.5-turbo-0125"
        self.model_location = "./artifacts/model.txt"
        self.training_data_location = "./artifacts/training_data.jsonl"
        self.user = user
        self.conversation_history = [
                {"role": "system", "content": f"""Aiza is a personal \
                        assistant customized for providing personal \
                        information about me ({self.user}).\
                """}
                ]

    def learn_user(self):
        if not path.exists(self.training_data_location):
            logging.error("Error: Must generate training_data.jsonl file \
                    before running this command.\n")
            return
        data_file = self.model.files.create(
            file=open(self.training_data_location, "rb"), purpose="fine-tune")
        job = self.model.fine_tuning.jobs.create(
            training_file=data_file.id, model=self.model_version)
        dot = "."
        while not (model := self.model.fine_tuning.jobs.retrieve(
                job.id).fine_tuned_model):
            logging.info(f"Learning user information{dot}")
            dot = "." if len(dot) == 5 else dot + "."
            sleep(60)
        with open(self.model_location, "w", encoding="utf-8") as file:
            file.write(model)
        logging.info("User has been successfully learned")

    def run(self):
        self.model_id = open(self.model_location, 'r').readlines()[0]
        logging.info("Aiza is ready! Type 'exit' to quit.\n")
        while (user_input := input("You: ")) != "exit":
            response = self._chat(user_input)
            logging.info(f"Assistant: {response}\n")
        logging.info("Exited conversation")

    def _chat(self, user_input):
        logging.debug(f'prompt: {user_input}')
        self.conversation_history.append(
                {"role": "user", "content": user_input})
        response = self.model.chat.completions.create(
            model=self.model_id, messages=self.conversation_history)
        reply = response.choices[0].message.content
        self.conversation_history.append(
                {"role": "assistant", "content": reply})
        logging.debug(f'reply: {reply}')
        return reply
