from data_loader.sources.templates.base_processor import BaseProcessor


class YouTube(BaseProcessor):
    def __init__(self, user, service, model):
        super().__init__(model)
        self.user = user
        self.service = service

    def get_data(self):
        results = self.service.activities().list(part="snippet", mine=True).execute()
        return [{"title": item["snippet"].get("title", "No Title Available"), "published": item["snippet"].get("publishedAt", "Unknown Date")} for item in results.get("items", [])]

    def process_data(self, data):
        print("\n🎥 **YouTube Watch History:**")
        for video in self.get_data()[0:5]:
            print(f"- {video['title']} (Published: {video['published']})")

    def _valid_data(self, data):
        pass

    def _generate_datapoints(self):
        pass
