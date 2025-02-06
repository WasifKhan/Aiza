from keys.keys import OPENAI_API_KEY
from openai import OpenAI 


class DataGenerator:
    def __init__(self):
        self.model = OpenAI(api_key=OPENAI_API_KEY)
        self.model_version = "gpt-4o"
        self.system_prompt = """You are a teacher. The user will provide long \
            unstructured text documents. Your goal is to generate questions \
            that could be asked about the text the user provided alongside the 
            associated correct answer. The answers should be detailed. Spend \
            time to think about the answer. Provide your response in the \
            exact format: "question: <question> answer: <answer>"\
            """

    def generate_data(self, data_source):
        """
        Provides interaction with GPT-4o by sending a user query 
        and receiving a response.
    
        :param data_source: User's data file as a string.
        :return: GPT-4o's response as a string.
        """
        message = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": data_source}
                ]
        response = self.model.chat.completions.create(
                model='gpt-4o', messages=message)
        reply = response.choices[0].message.content
        return reply
