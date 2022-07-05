import numpy as np
import json
import logging.config
import yaml


with open('..\config\master_config.yml', 'r') as config:
    logging.config.dictConfig(yaml.safe_load(config)['logging'])

main_logger = logging.getLogger('main')
error_logger = logging.getLogger('error')

class ScrapeDataAnalyzer():
    __file_path = '..\logs\output_data.json'
    __scrapped_data = []

    def __int__(self):
        main_logger.info('Scraped data analyzer instance created')

    def __getScrapeData(self):
        with open(self.__file_path, 'r') as f:
            scrape_data = json.load(f)
        return scrape_data

    def __getScrapeDataAsList(self, scrape_data):
        data_as_list = []
        for item in scrape_data:
            res = item[0].items()
            data_as_list.append(list(res))
        return data_as_list

    def __getArrayFilteredByEmptyData(self, data_arr):
        filter_arr = []
        for item in data_arr:
            if np.any(item == ""):
                filter_arr.append(False)
            else:
                filter_arr.append(True)
        filtered_data_arr = data_arr[filter_arr]
        return filtered_data_arr

    def __constructVariables(self):
        test = ScrapeDataAnalyzer()
        scrape_data = test.__getScrapeData()
        data_as_list = test.__getScrapeDataAsList(scrape_data)
        data_arr = np.array(data_as_list)
        filtered_data_arr = test.__getArrayFilteredByEmptyData(data_arr)
        self.__scrapped_data = filtered_data_arr
        pass

    def GetAveragePrice(self):
        try:
            ScrapeDataAnalyzer.__constructVariables(self)
            prices = []
            for item in self.__scrapped_data:
                prices.append(float(item[3][1]))
            avg_price = sum(prices) / len(prices)
            return avg_price
        except:
            error_logger.exception('Could not calculate the average price.')
            return 0

    def GetDataFilteredByMaxPrice(self, max_price):
        ScrapeDataAnalyzer.__constructVariables(self)
        data_out = []
        try:
            if float(max_price) > 0:
                filter_arr = []
                prices = []
                for item in self.__scrapped_data:
                    prices.append(float(item[3][1]))
                for item in prices:
                    if item >= float(max_price):
                        filter_arr.append(False)
                    else:
                        filter_arr.append(True)
                filtered_data_arr = self.__scrapped_data[filter_arr]
            else:
                filtered_data_arr = self.__scrapped_data
            for item in filtered_data_arr:
                data_formated = [
                    {item[0][0]: item[0][1], item[1][0]: item[1][1], item[2][0]: item[2][1],
                     item[3][0]: item[3][1]}]
                data_out.append(data_formated)
        except ValueError:
            error_logger.exception('Incorrect numeric value input was provided. Filtered file will be empty.')
        except:
            error_logger.exception('Something went wrong with data filtering. Filtered file will be empty.')
        finally:
            with open('..\logs\output_data_filtered.json', 'w') as f:
                json.dump(data_out, f, indent=4, ensure_ascii=False)
        pass