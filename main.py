from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome()


def wait_for_dropdown(select):
    if len(select.find_elements_by_tag_name("option")) > 1:
        return
    else:
        time.sleep(1)
        wait_for_dropdown(select)


def brand_selector(year_option):
    year_select = Select(driver.find_element_by_id("years"))
    year_select.select_by_value(year_option.text)

    brands = driver.find_element_by_id("brands")

    wait_for_dropdown(brands)
    brand_options = brands.find_elements_by_tag_name("option")

    for brand_option in brand_options:
        print(brand_option.text)

    return brand_options


def main():
    driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")

    years = driver.find_element_by_id("years")

    wait_for_dropdown(years)
    year_options = years.find_elements_by_tag_name("option")

    for year_option in year_options:
        if(year_option.text == "2019"):
            brand_selector(year_option)


main()

driver.close()
