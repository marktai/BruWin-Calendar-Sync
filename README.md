# BruWin-Calendar-Sync
BruWin is a UCLA app that gives you free points if you check into the events.  I used to make the Google Calendar events manually to remind myself, but then I made this Python program to automatically do it for me.  

## Installation
1) Install the Google API Python client:
```bash
sudo pip install --upgrade google-api-python-client
```
2) Also, get client_secret.json from https://console.developers.google.com/flows/enableapi?apiid=calendar
3) Clone the repository.

## Program Steps
1) Gets list of events from https://api.superfanu.com/3.1.0/gen/get_events.php?nid=45&headers=year
2) Parses the date into Google preferred format
3) Uploads the event to my calendar specifically for BruWin

## Notes
This is my first time using Vim, so my formatting might be a bit off.
