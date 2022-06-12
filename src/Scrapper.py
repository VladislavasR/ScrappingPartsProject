from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import logging.config
import yaml


with open('..\config\master_config.yml', 'r') as config:
    logging.config.dictConfig(yaml.safe_load(config)['logging'])

main_logger = logging.getLogger('main')
error_logger = logging.getLogger('error')

class RRRScrapper():
    def __int__(self):
        main_logger.info('RRR scrapper instance created')

    def ScrapeNameData(driver):
        sel_name = '* > ul > li > div > div > h3 > a'
        return driver.find_elements(By.CSS_SELECTOR, sel_name)

    def ScrapeInfoData(driver):
        sel_name = '* > ul > li > div > p'
        return driver.find_elements(By.CSS_SELECTOR, sel_name)

    def ScrapePriceData(driver):
        sel_price = 'products__price'
        return driver.find_elements(By.CLASS_NAME, sel_price)

    def ScrapeBySearchName(self, search_name):
        op = webdriver.ChromeOptions()
        with webdriver.Chrome(service=ChService('../drivers/chromedriver_v101.exe'), options=op) as driver:
            driver.get("https://rrr.lt/")

            delay = 20
            WebDriverWait(driver, delay).until(
                expected_conditions.element_to_be_clickable(
                    (By.NAME, 'q')
                )
            )
            elem = driver.find_element(by=By.NAME, value="q")
            elem.clear()
            time.sleep(1)
            elem.send_keys(search_name)
            time.sleep(1)

            try:
                elem_search = driver.find_elements(by=By.CLASS_NAME, value="search_autocomplete__list_links")[0]
                elem_search.send_keys(Keys.ENTER)
            except:
                error_logger.exception('No autocomplete results for this part name')
                elem.send_keys(Keys.ENTER)

            continue_to_scrape = True
            data_out = []

            while continue_to_scrape:
                delay = 20
                WebDriverWait(driver, delay).until(
                    expected_conditions.element_to_be_clickable(
                        (By.NAME, 'q')
                    )
                )

                too_many_results = driver.find_element(By.CLASS_NAME, 'part-count').text
                if len(too_many_results) > 4:
                    error_logger.exception('Too many results for this part name')
                    break

                parts_name = RRRScrapper.ScrapeNameData(driver)
                parts_info = RRRScrapper.ScrapeInfoData(driver)
                parts_prices = RRRScrapper.ScrapePriceData(driver)

                car_names = []
                part_codes = []
                adress = []

                i = 0
                for item in parts_info:
                    if i == 0:
                        car_names.append(item.text)
                        i += 1
                    elif i == 1:
                        part_codes.append(item.text)
                        i += 1
                    else:
                        adress.append(item.text)
                        i = 0

                for j in range(0, len(car_names)):
                    try:
                        data_formated = [{"Part Name": parts_name[j].text, "Car Name": car_names[j], "Part Code": part_codes[j], "Adress": adress[j], "Price": parts_prices[j].text}]
                        data_out.append(data_formated)
                    except:
                        break

                check_to_stop =  driver.find_elements(by=By.XPATH, value='//span[@class="pages__links disabled" and text()="Sekantis"]')
                if check_to_stop:
                    continue_to_scrape = False
                    break

                delay = 20
                WebDriverWait(driver, delay).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, '//a[@class="pages__links" and text()="Sekantis"]')
                    )
                )

                next_elem = driver.find_element(by=By.XPATH, value='//a[@class="pages__links" and text()="Sekantis"]')
                next_elem.send_keys(Keys.ENTER)


        with open('..\logs\output_data.json', 'w') as f:
            json.dump(data_out, f, indent=4, ensure_ascii=False)

        return len(data_out)