import MyScrapper
import DataAnalyzer
import logging
import yaml
import argparse

parser = argparse.ArgumentParser(description='rrr.lt parts scrapper')
help_str = 'method to call in the program (scrape)'
parser.add_argument('--method', required=False, type=str, nargs='?', help=help_str)
args = parser.parse_args()

with open('../config/master_config.yml', 'r') as config:
    yml_config = yaml.safe_load(config)
    logging.config.dictConfig(yml_config['logging'])
    config = yml_config['app']
logger = logging.getLogger('main')

print('Enter part name to search for in rrr.lt:')
search_name = input()
if search_name == "":
    search_name = "Toyota Distronikas"

print('Enter maximum price to filter out results:')
max_price = input()

parts_found = 0
scrapper = MyScrapper.RRRScrapper()
parts_found = scrapper.ScrapeBySearchName(search_name)

analyzer = DataAnalyzer.ScrapeDataAnalyzer()
avg_part_price = analyzer.GetAveragePrice()
analyzer.GetDataFilteredByMaxPrice(max_price)

method = config['method_to_illustrate'].upper() if args.method is None else args.method.upper()
logger.warning('{} : {}, {} : {}'.format(method + ' ' + search_name + ' parts found', parts_found,
                                         'average price', avg_part_price))