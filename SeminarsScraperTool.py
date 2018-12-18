from Log import Log
from seminars_web_scraper import WebScraper

log = Log()
log.create()
scraper = WebScraper(log)
url = 'https://www.ufrgs.br/ppgbioq/category/eventos/'
scraper.get_html(url)
log.close()
