from prompts.file_prompts import check_duplicate, valid_data, generate_facts, \
        generate_datapoints, input_msg
from data_loader.sources.templates.base_processor import BaseProcessor
from misc.logger import logger
from openai import OpenAI
from keys.keys import OPENAI_API_KEY
from io import BytesIO
from re import split
# import faiss

class Drive(BaseProcessor):
    def __init__(self, user, service, model, data, facts):
        super().__init__(model)
        self.user = user
        self.service = service
        self.data = data
        self.facts = facts
        self.files_processed = list()
        # self.embeddings = faiss.IndexFlatL2(1536)

    def get_data(self):
        query = "'root' in parents or mimeType " \
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
        facts = []
        for text in [content[i:i+5000] for i in range(0, len(content), 5000)]:
            if (dp := self._generate_facts(text)):
                facts.extend([f'{fact}\n' for fact in dp])
            if (dp := self._generate_datapoints(text)):
                datapoints.append(dp)
        datapoints = ''.join(datapoints)
        result = split(r'answer:\s*|question:\s*', datapoints)
        with open(self.data, 'a') as output:
            for index in range(2, len(result), 2):
                question, answer = self._format(result[index-1], result[index])
                # question, answer = self._generate_embeddings(question), self._generate_embeddings(answer)
                # print(f'embedding: {question}: {answer}')
                message = self._generate_input(question, answer)
                # self.embeddings.add(np.array([get_embedding("Hello, how are you?")]))  # Store vector
                output.write(message)
        with open(self.facts, 'a') as output:
            if facts:
                # facts = [f'[{", ".join([str(msg) for msg in self._generate_embeddings(fact)])[0:-2]}]\n' for fact in facts]
                output.writelines(facts)
        if datapoints:
            logger.log(f"Processed file: {data['name']}")
            self.files_processed.append(data['name'])

    def _valid_data(self, file_name, data):
        system_prompt = check_duplicate
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": 
                    f'{file_name}: ({", ".join(self.files_processed)})'}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        reply = response.choices[0].message.content.split()[0]
        if reply == "True":
            return False
        system_prompt = valid_data
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'{file_name}:\n{data}'}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        reply = response.choices[0].message.content.split()[0]
        return True if reply == "True" else False

    def _generate_facts(self, data):
        system_prompt = generate_facts
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message).choices[0]
        response = response.message.content.replace('False', '')
        return response.split('\n') if response else response

    def _generate_datapoints(self, data):
        system_prompt = generate_datapoints
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data}
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
            if not content or not self._valid_data(file_name, content[0:500]):
                raise Exception
        except Exception:
            logger.log(f'Cannot decode file: {file_name}', 'DEBUG')
            return []
        return content
        #return [self._generate_embeddings(text) for text in content]

    def _generate_input(self, question, answer):
        message = '{"messages": [{"role": "system", "content": '\
            f'"{input_msg}"}}, {{"role": "user", "content": "{question}"}}, '\
            f'{{"role": "assistant", "content": "{answer}"}}]}}\n'
        return message

    def _generate_embeddings(self, text):
        model = OpenAI(api_key=OPENAI_API_KEY)
        response = model.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
        
    def _format(self, question, answer):
        question = question.replace('\n', '').replace('"', "'")
        question = question[0:-2] if question[-2] == ' ' else \
            question[0:-1] if question[-1] == ' ' else question
        answer = answer.replace('\n', '').replace('"', "'")
        answer = answer[0:-2] if len(answer) > 1 and answer[-2] == ' ' \
            else answer[0:-1] if len(answer) >= 1 and answer[-1] == ' ' \
            else answer
        return question, answer
