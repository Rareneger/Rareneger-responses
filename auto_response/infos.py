import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd
import json

class Info():

    def __init__(self, data_id):
        self.data_id = data_id
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/documents']
        self.creds = self.google_login()
        self.data_dict = self.get_data_json()

    def get_email(self):
        return self.data_dict['email']['email']

    def get_email_password(self):
        return self.data_dict['email']['password']

    def get_pay_codes(self):
        return self.data_dict['pay codes']

    def get_last_timestamp(self):
        return self.data_dict['form']['last timestamp']

    def set_last_timestamp(self, timestamp):
        requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 163,
                    'endIndex': 182,
                    }
                }
            },
        ]
        service = build('docs', 'v1', credentials=self.creds)
        service.documents().batchUpdate(
        documentId=self.data_id, body={'requests': requests}).execute()

        requests = [{
            'insertText': {
                'location': {
                    'index': 163,
                },
                'text': timestamp
            }
        }]
        service.documents().batchUpdate(
        documentId=self.data_id, body={'requests': requests}).execute()

    def google_login(self):
        creds = None
        if os.path.exists('auto_response/personal-infos/token.json'):
            creds = Credentials.from_authorized_user_file('auto_response/personal-infos/token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'auto_response/personal-infos/client_secret.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('auto_response/personal-infos/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_form_df(self):
        service = build('sheets', 'v4', credentials=self.creds)

        sheet_id = self.data_dict['form']['sheet id']
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range='Respostas ao formulário 1').execute()
        values = result.get('values', [])

        # print(values)
        form_df = pd.DataFrame(values[1:], columns=values[0])
        return form_df

    def get_data_json(self):
        service = build('docs', 'v1', credentials=self.creds)
        document = service.documents().get(documentId=self.data_id).execute()
        str_json= self.read_strucutural_elements(document.get('body').get('content'))
        return json.loads(str_json)

    def read_strucutural_elements(self,elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += self.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += self.read_strucutural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += self.read_strucutural_elements(toc.get('content'))
        return text

    def read_paragraph_element(self, element):
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')
