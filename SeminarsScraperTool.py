from Log import Log
from seminars_web_scraper import WebScraper
from API_GoogleCal import GoogleCalAPI

log = Log()
log.create()
scraper = WebScraper(log)
url = 'https://www.ufrgs.br/ppgbioq/category/eventos/'
scraper.get_html(url)
seminars_list = scraper.get_data()
google_cal_api = GoogleCalAPI(log)
google_cal_api.create_events(seminars_list)
log.close()
