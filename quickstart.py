#!/usr/bin/python

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
    """ Unused function """
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
    """ Gets events from BruWin API
    Return JSON string"""
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("https://api.superfanu.com/3.1.0/gen/get_events.php?nid=45&headers=year", "GET")
    return json.loads(content)

    
def addEvent(service, calendar, summary, location, description, start, dayLightSaving):
    """Adds event to specified calendar if not already in there
    Returns true if event added, false otherwise"""
    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    if dayLightSaving:
	start = start + datetime.timedelta(minutes=60)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
        },
        'end': {
            'dateTime': (start + datetime.timedelta(minutes=30)).isoformat(),
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 0},
            ],
        },
    }
    
    eventsResult = service.events().list(
        calendarId=calendar, timeMin=(start + datetime.timedelta(minutes=-61)).isoformat(), maxResults=20, singleEvents=True,
        orderBy='startTime').execute()
    dupEvents = eventsResult.get('items', [])

    #many events can start at the same time
    #assumes no more than 20 start at the same time

    deleted = False
    for dupEvent in dupEvents:
        if dupEvent["summary"] == summary and dupEvent["location"] == location and dupEvent["description"] == description:
            deleted = True
	    service.events().delete(calendarId=calendar, eventId=dupEvent['id']).execute()
    event = service.events().insert(calendarId=calendar, body=event).execute()
    if not deleted:
        print ('Event created: %s %s' % (summary, start))
    else:
	print ('Event modified: %s %s' % (summary, start))
    return True

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events = getEvents()
	
    dayLightSaving = True;

    for event in events:
        timeString = event["date"] + " " + event["starttime"] + " -07:00"
        addEvent(service, "4hpackocjiu24bl06roa4ess6k@group.calendar.google.com", event["name"], event["description"], event["location"], parse(timeString), dayLightSaving) 


if __name__ == '__main__':
    main()

