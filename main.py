from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()


def wait_for_years(years):
    if len(years.find_elements_by_tag_name('option')) > 1:
        return
    else:
        time.sleep(1)
        wait_for_years(years)

def main():
    driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")

    years=driver.find_element_by_id("years")

    wait_for_years(years)
    print(len(years.find_elements_by_tag_name('option')))
    # for option in years.find_elements_by_tag_name('option'):
    #     print(option.text)


main()
