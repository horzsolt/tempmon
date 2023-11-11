import base64
import logging
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from requests import HTTPError

def sendMail(message: str) -> None:
    _logger = logging.getLogger(__name__)

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "gmail_client.json"), SCOPES
        )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message)
    message['to'] = 'horzsolt2006@gmail.com'
    message['subject'] = 'Tempmon mail sender'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(
            userId="me", body=create_message).execute())
        _logger.debug(f'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        _logger.debug(f'An error occurred: {error}')
        message = None
