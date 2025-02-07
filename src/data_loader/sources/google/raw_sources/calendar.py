from data_loader.sources.base_processor import BaseProcessor
from datetime import datetime


class Calendar(BaseProcessor):
    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_data(self):
        results = self.service.events().list(calendarId="primary").execute()
        return results.get("items", [])

    def process_data(self, data):
        print("\n📅 **Upcoming Google Calendar Events:**")
        for event in self.get_data()[0:5]:
            print(f"- {event.get('summary', 'No Title')} at {event['start'].get('dateTime', event['start'].get('date'))}")

    def _omit_junk_data(self, data):
        pass

    def _generate_datapoints(self):
        pass
