from data_loader.sources.sources import Sources
from data_loader.sources.google.raw_sources.drive import Drive
from data_loader.sources.google.raw_sources.mail import Mail
from data_loader.sources.google.raw_sources.maps import Maps
from data_loader.sources.google.raw_sources.calendar import Calendar
from data_loader.sources.google.raw_sources.youtube import YouTube
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


class Google(Sources):
    def __init__(self):
        super().__init__()
        self.scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/youtube.readonly"
            ]
        self.services = dict()
        self.key = "./keys/credentials.json"
        self.key_cache = "./keys/google_credentials.json"
        self.maps_location = "./data_loader/sources/google/Maps/\
                My labeled places/Labeled places.json"

    def authenticate(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.key, self.scopes)
        creds = flow.run_local_server(port=0)

        self.services['drive'] = Drive(
                build("drive", "v3", credentials=creds))
        self.services['mail'] = Mail(
                build("gmail", "v1", credentials=creds))
        self.services['maps'] = Maps(
                self.maps_location)
        self.services['calendar'] = Calendar(
                build("calendar", "v3", credentials=creds))
        self.services['youtube'] = YouTube(
                build("youtube", "v3", credentials=creds))

    def process(self):
        for key in self.services:
            print(f'\tProcessing google {key} services')
            service = self.services[key]
            files = service.get_data()
            for file in files:
                service.process_data(file)
