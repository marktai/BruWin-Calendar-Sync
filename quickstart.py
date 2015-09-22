from __future__ import print_function
import httplib2
import os
import json
import re
import datetime
from dateutil.parser import parse
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                     'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def parseInput(filePath):
    with open (filePath, "r") as contents:
        lines = contents.readlines()
            
        events = []
        event = {}
        started = False
        for line in lines:
            #print(line)
            if "<li id=" in line:
                started = True
            if started:
                if "<h3>" in line:
                    event["name"] = line.split("<h3>", 1)[1].split("</h3>",1)[0]

                if '<span class="date">' in line:
                    event["date"] = line.split('<span class="date">', 1)[1].split('</span>',1)[0]

                if "<p>" in line:
                    event["description"] = line.split("<p>", 1)[1].split("</p>",1)[0]

                if "</li>" in line:
                    started = False
                    events.append(event)
                    event = {}
        return events

def getEvents():

    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("https://api.superfanu.com/3.1.0/gen/get_events.php?nid=45&headers=year", "GET")
    return json.loads(content)
    #print(resp_headers)
    
def addEvent(service, calendar, summary, location, description, start):
    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': str(start).replace(" ", "T"),
        },
        'end': {
            'dateTime': str(start + datetime.timedelta(minutes=30)).replace(" ", "T"),
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 0},
            ],
        },
    }
    
    event = service.events().insert(calendarId=calendar, body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events = getEvents()
    event = events[0]
    for event in events:

        print(event)
        timeString = event["date"] + " " + event["starttime"] + " -07:00"
        print(parse(timeString))
        addEvent(service, "4hpackocjiu24bl06roa4ess6k@group.calendar.google.com", event["name"], event["description"], event["location"], parse(timeString)) 
        #print(parseInput("/home/mark/Downloads/Bruwin_Oct-31.txt"))

if __name__ == '__main__':
    main()

