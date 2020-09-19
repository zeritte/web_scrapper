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


def selector(selection_type, selection_value, newly_loaded):
    selection = Select(driver.find_element_by_id(selection_type))
    selection.select_by_value(selection_value.text)

    loaded_items = driver.find_element_by_id(newly_loaded)

    wait_for_dropdown(loaded_items)
    options = loaded_items.find_elements_by_tag_name("option")

    return options


def get_items():
    items = driver.find_element_by_xpath("/html/body/section/div[4]/div")
    print(items.get_attribute("innerHTML"))


def main():
    driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")
    find_button = driver.find_element_by_xpath(
        '//*[@id="find-battery"]/div[2]/button')

    years = driver.find_element_by_id("years")

    wait_for_dropdown(years)
    year_options = years.find_elements_by_tag_name("option")

    for year_option in year_options:
        if(year_option.text == "2018"):
            brand_options = selector("years", year_option, "brands")
            for brand_option in brand_options:
                if(brand_option.text == "VOLKSWAGEN"):
                    model_options = selector("brands", brand_option, "model")
                    for model_option in model_options:
                        if model_option.text == "PASSAT (3G2)":
                            submodel_options = selector(
                                "model", model_option, "altModel")
                            for submodel_option in submodel_options:
                                if submodel_option.text == "1.4 GTE Hybrid (115 kW / 156 PS)":
                                    submodel_selector = Select(
                                        driver.find_element_by_id("altModel"))
                                    submodel_selector.select_by_value(
                                        submodel_option.text)
                                    find_button = driver.find_element_by_xpath(
                                        '//*[@id="find-battery"]/div[2]/button')
                                    find_button.click()
                                    get_items()


main()

# driver.close()
