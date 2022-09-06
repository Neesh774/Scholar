import os
import json
from twilio.rest import Client
from notion_client import Client as NotionClient
import datetime


def format(string):
    if len(string) > 15:
        string = string[0:12] + ".."
    else:
        string = string + (" " * (14 - len(string)))
    return string


keys = json.load(open("keys.json", 'r'))

emojis = {
    "Unstarted": "🟥",
    "In Progress": "🟨"
}


def send():
    account_sid = keys['twilio_sid']
    auth_token = keys['twilio_auth']
    client = Client(account_sid, auth_token)

    notion = NotionClient(auth=keys['notion'])

    db = notion.databases.query(
        **{
            "database_id": keys['database'],
            "filter": {
                "and": [
                    {
                        "property": "Date",
                        "date": {
                            "equals": (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
                        }
                    },
                    {
                        "property": "Progress",
                        "select": {
                            "does_not_equal": "Completed"
                        }
                    }
                ]
            },
            "sorts": [
                {
                    "property": "Progress",
                    "direction": "descending"
                }
            ]
        }
    )['results']

    message = "\nHere are your assignments for " + \
        datetime.date.today().strftime("%a, %B %d") + ":\n"

    for page in db:
        title = format(page['properties']['Name']
                       ['title'][0]['text']['content'])
        subject = format(page['properties']['Subject']
                         ['rich_text'][0]['text']['content'])
        progress = emojis[page['properties']['Progress']['select']
                          ['name']] if page['properties']['Progress']['select'] else "🟦"
        message = message + progress + " | " + title + " | " + subject + "\n"

    # print(message)
    message = client.messages \
        .create(
            body=message,
            from_=keys['twilio_number'],
            to=keys['my_number'],
        )
    return message


def send_message():
    time = datetime.datetime.now()
    if time.hour == 14 and time.minute < 10 and time.minute > 1:
        print("Sending message...")
        message = send()
        print("Message Status", message.status)
        print('-' * 30)


if __name__ == "__main__":
    send()
