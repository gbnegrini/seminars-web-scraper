from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import bs4
from Log import Log
import re


class WebScraper:
    log = Log()

    def __init__(self, log):
        self.log = log

    def get_html(self, url):
        """Gets the url HTML content and parses it with BeautifulSoup"""
        self.log.write("Getting HTML...")
        try:
            html = urlopen(url)
            self.log.write("URL: <" + url + "> opened.")
            bs = bs4.BeautifulSoup(html.read(), "html.parser")
            self.log.write("HTML parsed.")
            # self.log.write("HTML: \n" + bs.prettify())
        except (HTTPError, URLError) as error:
            self.log.write(error.__str__())
            print(error)
