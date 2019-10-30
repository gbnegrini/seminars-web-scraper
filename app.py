from scraper import WebScraper
from api import GoogleCalAPI

scraper = WebScraper()
url = 'https://www.ufrgs.br/ppgbioq/category/eventos/'
scraper.get_html(url)
seminars_list = scraper.get_data()
api = GoogleCalAPI()
api.create_events(seminars_list)
