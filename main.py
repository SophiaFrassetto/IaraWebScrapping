# build-in imports
import logging

# project imports
from WebScrapping import WebScrappingController
from Exercises import sequencial_sum, remove_duplicate_char


logging.basicConfig(level=logging.INFO)


logging.info(f'\n{"#"*15} Test Web Scrapping {"#"*15}')
logging.info('Scraping page https://www.scrapethissite.com/pages/simple/')
# scrapping page https://www.scrapethissite.com/pages/simple/
WebScrappingController(url='https://www.scrapethissite.com/pages/simple/').process()

logging.info(f'\n{"#"*15} Exercise SUM {"#"*15}')
logging.info(f'Sequencial sum number 2: {sequencial_sum(2)}')
logging.info(f'Sequencial sum number 8: {sequencial_sum(8)}')
logging.info(f'Sequencial sum number 100000: {sequencial_sum(100000)}')

logging.info(f'\n{"#"*15} Exercise remove duplicate characters {"#"*15}')
duplicates = ["abracadabra", "allottee", "assessee", "kelless", "keenness", "Alfalggo"]
logging.info(f'Remove duplicate chars: {[remove_duplicate_char(x) for x in duplicates]}')
