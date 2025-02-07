from data_loader.sources.base_processor import BaseProcessor


class Mail(BaseProcessor):
    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_data(self):
            results = self.service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
            messages = []
            for msg in results.get("messages", []):
                msg_detail = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
                messages.append({"id": msg["id"], "snippet": msg_detail["snippet"]})
            return messages

    def process_data(self, data):
        print("\n📧 **Gmail Inbox:**")
        for email in self.get_data()[0:5]:
            print(f"- {email['snippet'][:100]}...")

    def _omit_junk_data(self, data):
        pass

    def _generate_datapoints(self):
        pass
