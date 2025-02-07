from data_loader.sources.base_processor import BaseProcessor
from keys.keys import GOOGLE_MAPS_API_KEY
from json import load
from googlemaps import Client

class Maps(BaseProcessor):
    def __init__(self, service):
        super().__init__()
        self.service = service

    def get_data(self):
        # Load the Google Takeout JSON file
        with open(self.service, "r", encoding="utf-8") as f:
            data = load(f)
        locations = data["features"]
        return locations

    def process_data(self, data):
        print("\n📍 **Google Maps Data:**")
        gmaps = Client(key=GOOGLE_MAPS_API_KEY)
        for place in self.fetch_google_maps()[0:5]:
            lat, lng = place["geometry"]["coordinates"][1], place["geometry"]["coordinates"][0]
            # Reverse geocode to get readable address
            reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
            address = reverse_geocode_result[0]["formatted_address"] if reverse_geocode_result else "Unknown Address"
            # Extract place name (if available)
            name = place["properties"].get("Title", "Unnamed Place")
            print(f"- 📍 {name} | 📌 {address} | 🗺️ Coordinates: {lat}, {lng}")

    def _omit_junk_data(self, data):
        pass

    def _generate_datapoints(self):
        pass
