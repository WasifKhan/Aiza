from data_loader.sources.templates.base_processor import BaseProcessor
from misc.logger import logger


class Mail(BaseProcessor):
    def __init__(self, user, service, model, data):
        super().__init__(model)
        self.user = user
        self.service = service
        self.data = data

    def get_data(self):
        results = self.service.users().messages().list(
                userId="me", 
                labelIds=["INBOX"]).execute()
        messages = []
        for msg in results.get("messages", []):
            msg_detail = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            messages.append({"id": msg["id"], "snippet": msg_detail["snippet"]})
        return messages

    def process_data(self, data):
        print(f"- {data['snippet'][:200]}...")


    def _valid_data(self, data):
        pass

    def _generate_facts(self, data):
        pass

    def _generate_datapoints(self):
        pass

    def _generate_embeddings(self, text):
        pass
