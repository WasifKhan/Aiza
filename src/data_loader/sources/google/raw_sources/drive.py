from data_loader.sources.base_processor import BaseProcessor
from misc.logger import logger
from io import BytesIO
from re import split


class Drive(BaseProcessor):
    def __init__(self, user, service, model):
        super().__init__(model)
        self.user = user
        self.service = service
        self.data = './artifacts/training_data.jsonl'

    def get_data(self):
        query = "'root' in parents or mimeType "\
                "!= 'application/vnd.google-apps.folder'"
        results = self.service.files().list(
                    q=query,
                    pageSize=1000,
                    fields="files(id, name, mimeType)").execute()
        all_files = results.get("files", [])
        return all_files

    def process_data(self, data):
        content = self._get_contents(data)
        datapoints = []
        for text in [content[i:i+5000] for i in range(0, len(content), 5000)]:
            if (dp := self._generate_datapoints(text)):
                datapoints.append(dp)
        datapoints = ''.join(datapoints)
        result = split(r'answer:\s*|question:\s*', datapoints)
        with open(self.data, 'a') as output:
            for index in range(2, len(result), 2):
                question, answer = self._format(result[index-1], result[index])
                message = self._generate_input(self.user, question, answer)
                output.write(message)
        if datapoints:
            logger.log(f"Processed file: {data['name']}")

    def _valid_data(self, data):
        system_prompt = "You are a personal document classifier. Your goal " \
                "is to determine if the content of a file contains personal " \
                f"information about {self.user}. This can be anything from " \
                "a diary, education information, work information, exercise " \
                "progress, among other things one would consider personal " \
                "information. The input will contain contents of a file. " \
                "Provide your response with just one word 'True' or 'False' " \
                "where True means the file contains personal information " \
                "and False otherwise. " \
                "For example: " \
                "input: 'Today was a tough day and I was depressed' and " \
                "output: 'True'. Another example: " \
                "input: 'letter-01 research-12-paper 543 fast-092.xlas' and " \
                "output: 'False'"
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        reply = response.choices[0].message.content.split()[0]
        return True if reply == "True" else False

    def _generate_datapoints(self, data_source):
        system_prompt = "You are a teacher. The user will provide long " \
            "unstructured text documents. Generate questions that could be " \
            "asked about the text the user provided alongside the " \
            "associated correct answer. Only include questions that test " \
            f"for personal information about {self.user}. If it is unclear " \
            f"who the text is about, assume it is about {self.user}. The " \
            "questions should be easy and phrased in first-tense such as " \
            "'How old am I?' not 'How old is Wasif'. The answers should be " \
            "concise. Spend time to think about the answer. " \
            "Provide your response in the exact format: " \
            "'question: <question> answer: <answer>'. If " \
            "personal information cannot be found, respond with 'False'. " \
            f"For example: input: '{self.user} is 32 years old, attends " \
            "university and enjoys working out.' output: " \
            "'question: How old am I? " \
            "answer: 32 years old. question: Am I enrolled in school? " \
            "answer: yes. question: what activity do I enjoy? answer: " \
            "working out'"
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data_source}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        return response.choices[0].message.content.replace('False', '')

    def _get_contents(self, data):
        file_id = data["id"]
        file_name = data["name"]
        mime_type = data["mimeType"]
        GOOGLE_DOC_EXPORTS = {
            "application/vnd.google-apps.document": "text/plain",
            "application/vnd.google-apps.spreadsheet": "text/csv",
            "application/vnd.google-apps.presentation": "text/plain"
        }
        content = []
        try:
            if mime_type in GOOGLE_DOC_EXPORTS:
                request = self.service.files().export_media(
                        fileId=file_id, mimeType=GOOGLE_DOC_EXPORTS[mime_type])
                content = request.execute().decode("utf-8")
            elif mime_type == "application/pdf":
                request = self.service.files().get_media(fileId=file_id)
                content = BytesIO(request.execute()).getvalue().decode("utf-8")
            elif mime_type.startswith("text/"):
                request = self.service.files().get_media(fileId=file_id)
                content = request.execute().decode("utf-8")
            if not content or not self._valid_data(content[0:300]):
                raise Exception
        except Exception:
            logger.log(f'Cannot decode file: {file_name}', 'DEBUG')
        return content

    def _generate_input(self, user, question, answer):
        message = '{"messages": [{"role": "system", "content": '\
            '"Aiza is a personal assistant cuztomized for '\
            'providing personal information about '\
            f'me ({self.user})."}}, '\
            f'{{"role": "user", "content": "{question}"}}, '\
            f'{{"role": "assistant", '\
            f'"content": "{answer}"}}]}}\n'
        return message

    def _format(self, question, answer):
        question = question.replace('\n', '').replace('"', "'")
        question = question[0:-2] if question[-2] == ' ' else \
            question[0:-1] if question[-1] == ' ' else question
        answer = answer.replace('\n', '').replace('"', "'")
        answer = answer[0:-2] if len(answer) > 1 and answer[-2] == ' ' \
            else answer[0:-1] if answer[-1] == ' ' else answer
        return question, answer
