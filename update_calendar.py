from notion_client import Client
import time
import datetime
import json

keys = json.load(open("keys.json", 'r'))
emojis = json.load(open("classIcons.json", "r"))


def create_page(name, description, subject, materials, id, link, date=None):
    icon = {
        "type": "emoji",
        "emoji": "📄"
    }
    for subj in emojis.keys():
        if subj in subject:
            icon['emoji'] = emojis[subj]
            break
    page = {
        "parent": {
            "database_id": keys['database']
        },
        "icon": icon,
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Subject": {
                "rich_text": [
                    {
                        "text": {
                            "content": subject
                        }
                    }
                ]
            },
            "id": {
                "rich_text": [
                    {
                        "text": {
                            "content": id
                        }
                    }
                ]
            },
            "Progress": {
                "select": {
                    "name": "Unstarted"
                }
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Assignment",
                                "link": {
                                    "type": "url",
                                    "url": link
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }

    if date:
        page["properties"]['Date'] = {
            "date": {
                "start": date
            }
        }
    if len(description) > 0:
        page['children'].append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": description
                            }
                        }
                    ]
            }
        },)
    if len(materials) > 0:
        page['children'].append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Materials"
                            }
                        }
                    ]
            }
        },)
    for material in materials:
        page['children'].append({
            "object": "block",
            "type": "bookmark",
            "bookmark": {
                "url": material
            }
        })
    page['children'].append({
        "object": "block",
        "type": "divider",
                "divider": {}
    })
    return page


def check_in_db(db, id):
    for page in db:
        # check if it has the id property
        if 'id' not in page['properties'].keys() or len(page['properties']['id']['rich_text']) == 0:
            continue
        if page['properties']['id']['rich_text'][0]['plain_text'] == id:
            return True
    return False


def update_calendar(assignments):
    notion = Client(auth=keys['notion'])

    db = notion.databases.query(
        **{
            "database_id": keys['database']
        }
    )['results']

    for i, course_name in enumerate(assignments.keys()):
        course_assignments = assignments[course_name]['assignments']
        percent_complete = int(20 * ((i+1) / len(assignments)))
        print('\r[' + ('\033[1;32m=\033[0;0m' * percent_complete) +
              ('=' * (len(assignments) - percent_complete)) + '] ' + str(i + 1) + '/' + str(len(assignments)) + ' Courses | ' + course_name, end=' ' * 40, flush=True)
        if len(course_assignments) == 0:
            time.sleep(0.2)
            continue
        for i in range(len(course_assignments)):
            assignment = course_assignments[i]
            assignment_name = assignment['title']
            if check_in_db(db, assignment['id']):
                continue

            if 'due' in assignment.keys():
                assignment_due_date = datetime.date.fromisoformat(
                    assignment['due'])

                # check if date is before today
                if assignment_due_date < datetime.date.today():
                    continue
                notion.pages.create(**create_page(
                    name=assignment_name, description=assignment['description'], link=assignment['link'], subject=course_name, materials=assignment['materials'], id=assignment['id'], date=assignment['due']))
            else:
                notion.pages.create(**create_page(
                    name=assignment_name, description=assignment['description'], link=assignment['link'], subject=course_name, materials=assignment['materials'], id=assignment['id']))


if __name__ == "__main__":
    assignments = json.load(open('courseWork.json', 'r'))
    update_calendar(assignments)
    print(
        '\rCompleted\033[1;32m Update Calendar\033[0;0m' + (" " * 40), end="\n")
