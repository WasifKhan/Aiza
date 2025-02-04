from openai import OpenAI
from models.base_model import BaseModel


class GPT(BaseModel):
    def __init__(self):
        self.model = OpenAI()
        self.conversation_history = []

    def start(self):
        print("YouAI is ready! Type 'exit' to quit.\n")
        while (user_input := input("You: ")) != "exit":
            response = self._chat(user_input)
            print(f"Assistant: {response}\n")
        print("Exited conversation")

    def _chat(self, user_input):
        self.conversation_history.append(
                {"role": "user", "content": user_input})

        response = self.model.chat.completions.create(
            model="gpt-4-turbo",
            messages=self.conversation_history
        )

        assistant_reply = response.choices[0].message.content
        self.conversation_history.append(
                {"role": "assistant", "content": assistant_reply})
        return assistant_reply
