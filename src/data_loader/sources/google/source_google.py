from data_loader.sources.sources import Sources
from json import load, dump
from googlemaps import Client
from requests import get
from io import BytesIO
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


class Google(Sources):
    def __init__(self):
        super().__init__()
# ====================================
# 1️⃣ Unified OAuth 2.0 Authentication
# ====================================
        self.scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/youtube.readonly"
            ]
        self.authenticate()
        print("\n📂 **Google Drive Files:**")
        for file in self.fetch_google_drive()[0:5]:
            print(f"- {file['name']} (ID: {file['id']})")

        print("\n📧 **Gmail Inbox:**")
        for email in self.fetch_gmail()[0:5]:
            print(f"- {email['snippet'][:100]}...")  # Print email snippet

        print("\n📅 **Upcoming Google Calendar Events:**")
        for event in self.fetch_google_calendar()[0:5]:
            print(f"- {event.get('summary', 'No Title')} at {event['start'].get('dateTime', event['start'].get('date'))}")

        print("\n🎥 **YouTube Watch History:**")
        for video in self.fetch_youtube_history()[0:5]:
            print(f"- {video['title']} (Published: {video['published']})")

        print("\n📍 **Google Maps Data:**")
        GOOGLE_MAPS_API_KEY = "AIzaSyD24roaOJMBMWlbQty4s8PLxsp60To5BKc"
        gmaps = Client(key=GOOGLE_MAPS_API_KEY)
        for place in self.fetch_google_maps()[0:5]:
            lat, lng = place["geometry"]["coordinates"][1], place["geometry"]["coordinates"][0]
            # Reverse geocode to get readable address
            reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
            address = reverse_geocode_result[0]["formatted_address"] if reverse_geocode_result else "Unknown Address"
            # Extract place name (if available)
            name = place["properties"].get("Title", "Unnamed Place")
            print(f"- 📍 {name} | 📌 {address} | 🗺️ Coordinates: {lat}, {lng}")


    def authenticate(self):
# Authenticate using OAuth (Single Authentication for all APIs)
        flow = InstalledAppFlow.from_client_secrets_file("./data_loader/sources/google/credentials.json", self.scopes)
        creds = flow.run_local_server(port=0)

# Reuse credentials for all Google API services
        self.services = {
            "drive": build("drive", "v3", credentials=creds),
            "gmail": build("gmail", "v1", credentials=creds),
            "calendar": build("calendar", "v3", credentials=creds),
            "youtube": build("youtube", "v3", credentials=creds)
        }

    def load_source(self):
        pass
# ====================================
# 2️⃣ Fetch Google Drive Data
# ====================================
    def fetch_google_drive(self):
        """Fetches all files and folders from Google Drive."""
        drive_service = self.services["drive"]
        query = "'root' in parents or mimeType != 'application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
        all_files = results.get("files", [])

        # Define export formats for Google Docs formats
        GOOGLE_DOC_EXPORTS = {
            "application/vnd.google-apps.document": "text/plain",  # Google Docs → Plain Text
            "application/vnd.google-apps.spreadsheet": "text/csv",  # Google Sheets → CSV
            "application/vnd.google-apps.presentation": "text/plain"  # Google Slides → Plain Text
        }

        def process_file(file):
            """Processes a file from Google Drive without downloading it."""
            file_id = file["id"]
            file_name = file["name"]
            mime_type = file["mimeType"]

            print(f"📂 Processing: {file_name} ({mime_type})")

            if mime_type in GOOGLE_DOC_EXPORTS:
                # Google Docs, Sheets, and Slides: Export & Process as text
                request = drive_service.files().export_media(fileId=file_id, mimeType=GOOGLE_DOC_EXPORTS[mime_type])
                file_content = request.execute().decode("utf-8")
                print(f"📜 Extracted Content (Google Doc/Sheet): {file_content[:500]}...\n")

            elif mime_type.startswith("image/"):
                # Image Processing: Just log (OCR or AI processing can be done here)
                print(f"🖼️ Skipping image file: {file_name}")

            elif mime_type == "application/pdf":
                # PDF Processing: Extract text without saving
                request = drive_service.files().get_media(fileId=file_id)
                file_content = BytesIO(request.execute())  # Stream content
                print(f"📄 PDF processed: {file_name} (Size: {len(file_content.getvalue())} bytes)\n")

            elif mime_type.startswith("text/"):
                # Plain text files: Read content
                request = drive_service.files().get_media(fileId=file_id)
                file_content = request.execute().decode("utf-8")
                print(f"📝 Text File Content: {file_content[:500]}...\n")

            else:
                print(f"⚠️ Unsupported file type: {mime_type}")
        return all_files
            


# ====================================
# 3️⃣ Fetch Gmail Data
# ====================================
    def fetch_gmail(self):
        gmail_service = self.services["gmail"]
        results = gmail_service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        messages = []
        for msg in results.get("messages", []):
            msg_detail = gmail_service.users().messages().get(userId="me", id=msg["id"]).execute()
            messages.append({"id": msg["id"], "snippet": msg_detail["snippet"]})
        return messages

# ====================================
# 4️⃣ Fetch Google Calendar Events
# ====================================
    def fetch_google_calendar(self):
        calendar_service = self.services["calendar"]
        results = calendar_service.events().list(calendarId="primary").execute()
        return results.get("items", [])


# ====================================
# 6️⃣ Fetch YouTube Watch History
# ====================================
    def fetch_youtube_history(self):
        youtube_service = self.services["youtube"]
        results = youtube_service.activities().list(part="snippet", mine=True).execute()
        return [{"title": item["snippet"].get("title", "No Title Available"), "published": item["snippet"].get("publishedAt", "Unknown Date")} for item in results.get("items", [])]

# ====================================
# 7️⃣ Fetch Google Maps Data (Separate API Key)
# ====================================
    def fetch_google_maps(self):
        # Load the Google Takeout JSON file
        with open("./Maps/My labeled places/Labeled places.json", "r", encoding="utf-8") as f:
            data = load(f)

        # Extract first 5 pinned locations
        locations = data["features"]

        return locations

        

