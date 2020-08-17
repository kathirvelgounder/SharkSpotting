from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
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
            print("token.pickle file found, attempting to use it for authentication.")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if not creds:
                print("token.pickle file not found, generating credentials for future use.")
            if creds and not creds.valid:
                print("Credentials not valid.")
            if creds and creds.expired:
                print("Credentials expired.")
            if creds and creds.refresh_token:
                print("Found refresh token.")
            if creds and creds.expired and creds.refresh_token:
                print("Attempting to refresh authentication.")
                try:
                    creds.refresh(Request())
                except RefreshError: #delete token.pickle and try again
                    print("Encountered token refresh error, try deleting token.pickle file and run again.")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        print("Successfully authenticated.")

        self.drive_service = build('drive', 'v3', credentials=creds)

        print("Successfully connected to drive.")

        



    def get_file_stream_by_id(self, file_id, mime_type):
        request = self.drive_service.files().get_media(fileId=file_id)
        stream = io.BytesIO()
        downloader = MediaIoBaseDownload(stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return stream


    
    def get_file_stream_by_name(self, file_name, mime_type):
        file_info = self.search_file_by_name(100, file_name)
        if file_info:
            stream = self.get_file_stream_by_id(file_info['id'], mime_type)
            return stream
            

    # TODO: figure out way to search without page size, i.e. just search all files in your drive...
    def search_file_by_name(self, size, file_name):
        query = "name contains '" + file_name + "'"
        results = self.drive_service.files().list(pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
        items = results.get('files', [])
        if len(items) == 0:
            print("No results found for file {}".format(file_name))
            return None
        elif len(items) > 1:
            print("Multiple results found for this file name, returning the first.")
        return items[0]

    def get_file_by_id(self, file_id, mime_type):
        request = self.drive_service.files().get_media(fileId=file_id)
        stream = io.BytesIO()
        downloader = MediaIoBaseDownload(stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return stream

    #download file locally
    def get_file_by_name(self, file_name, mime_type):
        file_info = self.search_file_by_name(100, file_name)
        if file_info:
            stream = self.get_file_by_id(file_info['id'], mime_type)
            return stream
