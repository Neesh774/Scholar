from __future__ import print_function

import os.path


from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from get_course_work import get_course_work
from update_calendar import update_calendar
from send_message import send_message

SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.coursework.me",
          "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly", "https://www.googleapis.com/auth/classroom.courses"]


def getCreds():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def main():
    creds = getCreds()
    print(('-' * 30))
    print('Starting\033[1;36m Scholar\033[0;0m')
    print('-' * 30)
    assignments = get_course_work(creds)
    print('\rCompleted\033[1;32m Get Course Work\033[0;0m' + (' ' * 30))
    print(('-' * 30))
    update_calendar(assignments)
    print(
        '\rCompleted\033[1;32m Update Calendar\033[0;0m' + (" " * 40), end="\n")
    print(('-' * 30))
    send_message()
    print('\033[1;36mScholar\033[0;0m Complete')


if __name__ == "__main__":
    main()
