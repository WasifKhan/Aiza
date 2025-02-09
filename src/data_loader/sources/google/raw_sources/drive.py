from data_loader.sources.templates.base_processor import BaseProcessor
from misc.logger import logger
from io import BytesIO
from re import split


class Drive(BaseProcessor):
    def __init__(self, user, service, model, data, facts):
        super().__init__(model)
        self.user = user
        self.service = service
        self.data = data
        self.facts = facts
        self.files_processed = list()

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
                facts.append(dp)
            if (dp := self._generate_datapoints(text)):
                datapoints.append(dp)
        datapoints = ''.join(datapoints)
        result = split(r'answer:\s*|question:\s*', datapoints)
        with open(self.data, 'a') as output:
            for index in range(2, len(result), 2):
                question, answer = self._format(result[index-1], result[index])
                message = self._generate_input(self.user, question, answer)
                output.write(message)
        with open(self.facts, 'a') as output:
            if facts:
                output.writelines(facts)
        if datapoints:
            logger.log(f"Processed file: {data['name']}")
            self.files_processed.append(data['name'])

    def _valid_data(self, file_name, data):
        system_prompt = "You are to determine if a given file name is similar " \
                "to any file name in a list of files. The user input will " \
                "contain a file name followed by a list of file names in " \
                "enclosed in brackets separated by commas. Output True if " \
                "the file name is similar to a file name in the list and " \
                "False otherwise. " \
                "For example: " \
                "input: 'Resume (cover letter, timeline, paper)' and " \
                "output: False. Another example: " \
                "input: 'Cover Letter (resume, edu-cover letter, research)' " \
                "and " \
                "output: True. Another example: " \
                "input: 'Timeline (timeline-long, resume, cover letter)' and " \
                "output: True."
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
        system_prompt = "You are a personal document classifier. You will " \
                "be provided the name of the file followed by some contents " \
                "of the file and you need to determine " \
                "if the contents of a file contains valuable information or " \
                "if it is code/AI generated/junk. This can be anything from " \
                "a diary, resume, transcript, exercise info, nutritional " \
                "information, among other things one would consider valuable " \
                "information. Documents containing dates/times are " \
                "considered valuable. " \
                "Provide your response with just one word 'True' or 'False' " \
                "where True means the file contains personal information " \
                "and False otherwise. If you are unsure, assume False." \
                "For example: " \
                "input: 'Resume:\nWasif Khan Resume 5 years experience' and " \
                "output: True. Another example: " \
                "input: 'research-12-paper:\nThis paper discusses the side " \
                "effects of model distillation.' and " \
                "output: False. Another example: " \
                "input: 'Timeline:\n1992-2001 School\n2000 Lost " \
                "virginity. 2003-2007 Worked.' and " \
                "output: True."
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'{file_name}:\n{data}'}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        reply = response.choices[0].message.content.split()[0]
        return True if reply == "True" else False

    def _generate_facts(self, data):
        system_prompt ="You are a fact generator. " \
            "The user will provide long unstructured text " \
            f"documents. Assume the text is about {self.user}. " \
            "Generate facts about {self.user}, one fact per " \
            "line. Focus on providing facts that includes names of friends, " \
            "family, work companies, job titles, dynamics of relationships, " \
            "locations and times of events. Provide facts in third person " \
            "as opposed to first person. Ie. 'He is 32 years old', not " \
            f"'{self.user} is 32 years old.'. If the text contains no " \
            f"facts about {self.user}, output 'False'."
        message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data}
                ]
        response = self.model.chat.completions.create(
                model=self.model_version, messages=message)
        return response.choices[0].message.content.replace('False', '')

    def _generate_datapoints(self, data):
        system_prompt = "You are a teacher. The user will provide long " \
            "unstructured text documents. Generate questions that could be " \
            "asked about the text the user provided alongside the " \
            "associated correct answer. Only include questions that test " \
            f"for personal information about {self.user}. Try to include " \
            f"dates, and names of other family and friends in {self.user}'s " \
            "life as part of the questions and answers where possible. " \
            "The " \
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
            else answer[0:-1] if len(answer) >= 1 and answer[-1] == ' ' \
            else answer
        return question, answer
