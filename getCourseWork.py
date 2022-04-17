from __future__ import print_function

import datetime
import dateutil.parser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.courses",
          "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly", "https://www.googleapis.com/auth/classroom.coursework.me"]


def getMaterials(courseWork):
    if 'materials' not in courseWork.keys():
        return []
    materials = courseWork['materials']
    res = []
    for material in materials:
        if 'link' in material.keys():
            res.append(material['link']['url'])
        elif 'driveFile' in material.keys():
            res.append(material['driveFile']['driveFile']['alternateLink'])
    return res


def getCourseWork(creds):
    try:
        service = build('classroom', 'v1', credentials=creds)
        courses = []
        page_token = None
        courseWork = {}

        while True:
            response = service.courses().list(pageToken=page_token,
                                              pageSize=20, courseStates=["ACTIVE"], studentId="me").execute()
            courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        for i, course in enumerate(courses):
            percent_complete = int(20 * ((i+1) / len(courses)))
            print('\r[' + ('\033[1;32m=\033[0;0m' * percent_complete) +
                  ('=' * (len(courses) - percent_complete)) + '] ' + str(i + 1) + '/' + str(len(courses)) + ' Courses | ' + course['name'], end=' ' * 40, flush=True)
            coursework = service.courses().courseWork().list(
                courseId=course.get('id'),
                orderBy="dueDate desc",
                pageSize=100
            ).execute()
            if('courseWork' not in coursework.keys()):
                continue
            coursework = coursework['courseWork']
            assignments = []
            for work in coursework:
                created = dateutil.parser.isoparse(work['creationTime']).date()
                delta = datetime.timedelta(days=90)
                if created + delta < datetime.date.today():
                    continue
                new_work = {
                    "title": work['title'],
                    "description": work['description'] if ('description' in work.keys()) else ''
                }
                due = None
                if 'dueDate' in work.keys():
                    year = work['dueDate']['year']
                    month = work['dueDate']['month']
                    day = work['dueDate']['day']
                    new_due = datetime.date(year, month, day)
                    if new_due < datetime.date.today():
                        continue
                    new_work['due'] = new_due.isoformat()
                new_work['link'] = work['alternateLink']
                new_work['materials'] = getMaterials(work)
                new_work['id'] = work['id']
                assignments.append(new_work)
            courseWork[course['name']] = {
                "course_id": course['id'],
                "assignments": assignments
            }
        with open('courseWork.json', 'w') as assignments:
            assignments.write(json.dumps(courseWork))
        return courseWork
    except HttpError as error:
        print(error)
        return error
