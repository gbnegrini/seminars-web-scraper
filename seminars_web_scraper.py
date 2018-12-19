from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import bs4
from Log import Log
from Seminar import Seminar
import re
from datetime import datetime
import traceback
import sys
from pprint import pprint


class WebScraper:
    log = Log()
    bs = None

    def __init__(self, log):
        self.log = log

    def get_html(self, url):
        """Gets the url HTML content and parses it with BeautifulSoup"""
        self.log.write("Getting HTML...")
        try:
            html = urlopen(url)
            self.log.write("URL: <" + url + "> opened.")
            self.bs = bs4.BeautifulSoup(html.read(), "html.parser")
            self.log.write("HTML parsed.")
            # self.log.write("HTML: \n" + bs.prettify())
        except (HTTPError, URLError) as error:
            self.log.write("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.log.write(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))

    def get_data(self):
        """Does all the magic to extract the seminars information"""
        try:
            # Gets all <articles> tag
            articles_list = self.bs.find_all("article")
            seminar_event = Seminar()
            seminars = []

            for article in articles_list:

                seminar_event.summary = " ".join(article.h2.getText().split()[0:-3])
                seminar_event.description = article.p.getText() \
                                            + "\nLink: " + article.a.get("href")

                # Regex expressions to get hour, minutes and date from the article tag text
                hour_regex = re.compile(r'.\dh')
                minutes_regex = re.compile(r'\d.min')
                date_regex = re.compile(r'.\d/.\d')

                # Gets the text matching the date regex expression and splits into day and month
                day, month = date_regex.search(article.h2.getText()).group().split("/")

                # Gets the hours matching the hour regex expression, splits into the "h" delimiter and removes white space
                hour = hour_regex.search(article.h2.getText()).group().split("h")[0].replace(" ", "")
                if (int(hour) < 10):    # If the hour has only one digit
                    hour = "0"+hour     # then a zero must be added to match the dateTime template

                try:
                    # Gets the minutes matching the minutes regex expression, splits into the "min" delimiter
                    minutes = minutes_regex.search(article.h2.text).group().split("min")[0]
                except AttributeError:
                    minutes = "00"      # Sometimes the minutes digits are absent so define it as "00"

                # dateTime template : YYYY-MM-DDTHH:MM:SS-02:00
                seminar_event.start = str(datetime.today().year)+"-"+month+"-"+day+"T"+hour+":"+minutes+"00"+"-2:00"
                end_hour = str(int(hour)+1)  # Seminars usually last one hour
                seminar_event.end = str(datetime.today().year)+"-"+month+"-"+day+"T"+end_hour+":"+minutes+"00"+"-2:00"

                # Adds the seminar object to the seminars list
                seminars.append(seminar_event)

                self.log.write("The following seminar was added to the list: ")
                for parameter in seminar_event.seminar_parameters():
                    self.log.write(parameter)

        except Exception as error:
            self.log.write("Error: " + error.__str__())
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.log.write(str(traceback.format_exception(exc_type, exc_value, exc_tb)))
            pprint(traceback.format_exception(exc_type, exc_value, exc_tb))