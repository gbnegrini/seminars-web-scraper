from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import traceback
import sys
from pprint import pprint
import re

class GoogleCalAPI:
    """# Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/calendar/quickstart/python"""

    gcal = None
    #calID = 'm6ontqrghi0omg8vnuo8i6daac@group.calendar.google.com'
    calID = 'r00mr8gkk0mpg2ia01e8mbd66g@group.calendar.google.com'

    def __init__(self):
        try:
            SCOPES = 'https://www.googleapis.com/auth/calendar'
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)
            self.gcal = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

            print("API authorization flow completed.")

        except Exception as error:
            print("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_events_links(self):
        '''Gets the events already registered in the calendar'''
        link_regex = re.compile(r'<.*>')
        page_token = None
        link_list = []
        while True:
            event = self.gcal.events().list(calendarId=self.calID, singleEvents=True, pageToken=page_token).execute()
            for event in event['items']:
                try:
                    # the unique link for the seminar's institutional page will be used further to avoid adding the same event again
                    link = link_regex.search(event['description']).group()
                    link_list.append(link)
                except AttributeError:
                    pass
            page_token = event.get('nextPageToken')

            if not page_token:
                break
        print(len(link_list))
        return link_list

    def create_events(self, seminars_list):
        try:

            link_list = self.get_events_links()

            for seminar in seminars_list:

                try:
                    # checks if this seminar is not already in the calendar, if it isn't then creates the event
                    if seminar.link not in link_list:

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
                        print('Event created: %s' % (event.get('htmlLink')))
                        print(event.get('summary') + "\n" + event.get('description'))
                        print('Event created: %s' % (event.get('htmlLink')))
                except TypeError:
                    pass

        except Exception as error:
            print("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))
