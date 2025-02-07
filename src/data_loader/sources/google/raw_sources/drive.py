from data_loader.sources.base_processor import BaseProcessor
from io import BytesIO
from re import split


class Drive(BaseProcessor):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.data_location = './artifacts/training_data.jsonl'

    def get_data(self):
        query = "'root' in parents or mimeType "\
                "!= 'application/vnd.google-apps.folder'"
        results = self.service.files().list(
                q=query,
                pageSize=1000,
                fields="files(id, name, mimeType)").execute()
        all_files = results.get("files", [])
        return self._omit_junk_data(all_files)

    def process_data(self, data):
        file_id = data["id"]
        file_name = data["name"]
        mime_type = data["mimeType"]
        GOOGLE_DOC_EXPORTS = {
            "application/vnd.google-apps.document": "text/plain",
            "application/vnd.google-apps.spreadsheet": "text/csv",
            "application/vnd.google-apps.presentation": "text/plain"
        }
        if mime_type in GOOGLE_DOC_EXPORTS:
            request = self.service.files().export_media(
                    fileId=file_id, mimeType=GOOGLE_DOC_EXPORTS[mime_type])
            file_content = request.execute().decode("utf-8")
            print(f"\t\tDoc processed: {file_name}")
        elif mime_type.startswith("image/"):
            print('\t\tSkipped Image')
            return None
        elif mime_type == "application/pdf":
            request = self.service.files().get_media(fileId=file_id)
            file_content = BytesIO(request.execute())  # Stream content
            print(f"\t\tPDF processed: {file_name}")

        elif mime_type.startswith("text/"):
            request = self.service.files().get_media(fileId=file_id)
            file_content = request.execute().decode("utf-8")
            print(f"\t\tText File processed: {file_name}")

        else:
            print(f"\t\tUnsupported file type: {mime_type}")
            return None
        datapoints = self._generate_datapoints(file_content)
        result = split(r'\n{1,2}', datapoints)
        with open(self.data_location, 'a') as output:
            for index in range(len(result)):
                if index % 2:
                    question = result[index-1][10:-2]
                    answer = result[index][8:]
                    message = '{"messages": [{"role": "system", "content": '\
                            '"Aiza is a personal assistant that gathers as '\
                            'much personal information about a user as '\
                            'possible."}, '\
                            f'{{"role": "user", "content": "{question}"}}, '\
                            f'{{"role": "assistant", '\
                            f'"content": "{answer}"}}]}}\n'
                    output.write(message)

    def _omit_junk_data(self, data):
        system_prompt = """You are to analyze file names to determine if they \
                are files that a person would have created versus files that \
                are either code generated, generated by an AI, just a file \
                that seems accidently created or doesn't seem like it's \
                contents would be valuable. The input will contain file names \
                separated by a space. Provide your response with just \
                space separated "True" or "False" values respectively, where \
                True means the file is a file that a person would have \
                created, and False otherwise. If you are unsure, lean on the \
                side of labeling it False. For example: \
                input: "diary test01 banking doc-fjakd-o2ts3m letter.zip" and \
                output: "True False True False False". Another example: \
                input: "chat_history calls letter-01 research-124-paper\
                logs datapoints.zip my_first game-history.zip lover" and \
                output: "True True False False False False False True"\
                """
        file_names = ' '.join([file['name'] for file in data])
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": file_names}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        valid_files = []
        reply = response.choices[0].message.content.split()
        for index in range(len(reply)):
            if reply[index] == "True":
                valid_files.append(data[index])
        return valid_files

    def _generate_datapoints(self, data_source):
        system_prompt = """You are a teacher. The user will provide long \
            unstructured text documents. Your goal is to generate questions \
            that could be asked about the text the user provided alongside \
            the associated correct answer. The question should be easy. \
            The answers should be concise. This isn't meant to be tricky. \
            Spend time to think about the answer. Provide your response in \
            the exact format: "question: <question> answer: <answer>"\
            """
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data_source}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        return response.choices[0].message.content
