from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

'''
NOTE BEFORE USING FOR THE FIRST TIME:

Follow steps 1 and 2 from this Google Drive Python API set up - https://developers.google.com/drive/api/v3/quickstart/python

Then, move the credentials.json file into the same directory as this file.

Make sure that the file you want to access is under your 'My Drive'

'''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class DriveConnection:

    # creates a "drive_service" object that you need to perform actions in the Google Drive API
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            print("Found Google Drive authentication in token.pickle file.")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            print("No Google Drive authentication found yet (token.pickle file not present).")
            print("Generating credentials to store for future use.")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.drive_service = build('drive', 'v3', credentials=creds)
        



    def getFileById(self, file_id, mime_type):
        request = self.drive_service.files().get_media(fileId=file_id)
        stream = io.BytesIO()
        downloader = MediaIoBaseDownload(stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return stream


    def getFileByName(self, file_name, mime_type):
        file_info = searchFileByName(100, file_name)
        return getFileById(file_info['id'], mime_type)

    # TODO: figure out way to search without page size, i.e. just search all files in your drive...
    def searchFileByName(self, size, file_name):
        query = "name contains '" + file_name + "'"
        results = self.drive_service.files().list(pageSize=size,
                                            fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
        items = results.get('files', [])
        if len(items) == 0:
            print("No results found for this file name.")
            return None
        elif len(items) > 1:
            print("Multiple results found for this file name, returning the first.")
        return items[0]
