from data_loader.sources.templates.base_source import BaseSource
from data_loader.sources.google.raw_sources.drive import Drive
from data_loader.sources.google.raw_sources.mail import Mail
from data_loader.sources.google.raw_sources.maps import Maps
from data_loader.sources.google.raw_sources.calendar import Calendar
from data_loader.sources.google.raw_sources.youtube import YouTube
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from misc.logger import logger


class Google(BaseSource):
    def __init__(self, user, model, data, facts):
        self.scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/youtube.readonly"
            ]
        self.user = user
        self.model = model
        self.data = data
        self.facts = facts
        self.key = "./keys/google_credentials.json"
        self.services = dict()

    def authenticate(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.key, self.scopes)
        creds = flow.run_local_server(port=0)
        user = self.user
        self.services['drive'] = Drive(
                                    user,
                                    build("drive", "v3", credentials=creds),
                                    self.model,
                                    self.data,
                                    self.facts)
        '''
        self.services['mail'] = Mail(user,
                                     build("gmail", "v1", credentials=creds),
                                     self.model,
                                     self.data)
        self.services['maps'] = Maps(
                user, self.maps, self.model)
        self.services['calendar'] = Calendar(
                user, build("calendar", "v3", credentials=creds), self.model)
        self.services['youtube'] = YouTube(
                user, build("youtube", "v3", credentials=creds), self.model)
        '''

    def process(self):
        for key in self.services:
            logger.log(f'Processing google {key} services')
            service = self.services[key]
            files = service.get_data()
            for file in files:
                service.process_data(file)
