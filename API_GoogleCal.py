from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from Log import Log
import traceback
import sys
from pprint import pprint
from Seminar import Seminar


class GoogleCalAPI:
    """# Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/calendar/quickstart/python"""
    log = Log()
    gcal = None
    calID = '9tg5lsgki4v4o1hib2q6js23hc@group.calendar.google.com'

    def __init__(self, log):
        try:
            self.log = log

            SCOPES = 'https://www.googleapis.com/auth/calendar'
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            self.gcal = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

            self.log.write("API authorization flow completed.")

        except Exception as error:
            self.log.write("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.log.write(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))

    def create_events(self, seminars_list):
        try:
            for seminar in seminars_list:
                print(seminar.summary)
                event = {
                    'summary': seminar.summary,
                    'description': seminar.description,
                    'start': {
                        'dateTime': seminar.start
                    },
                    'end': {
                        'dateTime': seminar.end
                    }
                }

                event = self.gcal.events().insert(calendarId=self.calID, body=event).execute()
                self.log.write('Event created: %s' % (event.get('htmlLink')))
                self.log.write(event.get('summary') + "\n" + event.get('description'))
                print('Event created: %s' % (event.get('htmlLink')))

        except Exception as error:
            self.log.write("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.log.write(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))