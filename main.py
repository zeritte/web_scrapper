from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome()

result = []


def wait_for_dropdown(select):
    if len(select.find_elements_by_tag_name("option")) > 1:
        return
    else:
        time.sleep(1)
        wait_for_dropdown(select)


def selector(selection_type, selection_value, newly_loaded):
    selection = Select(driver.find_element_by_id(selection_type))
    selection.select_by_value(selection_value)

    loaded_items = driver.find_element_by_id(newly_loaded)

    wait_for_dropdown(loaded_items)
    options = loaded_items.find_elements_by_tag_name("option")

    return options[1:]


def get_items(year_option, brand_option, model_option, submodel_option):
    parent_element = driver.find_element_by_xpath(
        "/html/body/section/div[4]/div")
    element_list = parent_element.find_elements_by_tag_name("a")

    for element in element_list:
        element_data = {}
        element_data["url"] = driver.current_url
        element_data["year"] = year_option
        element_data["brand"] = brand_option
        element_data["model"] = model_option
        element_data["submodel"] = submodel_option

        type_ = element.find_element_by_class_name("uk-text-bolder")
        if type_.get_attribute("innerHTML").startswith("TAVSİYE"):
            type_ = "TAVSİYE EDİLEN"
        else:
            type_ = type_.get_attribute("innerHTML")
        element_data["type"] = type_

        name = element.find_element_by_class_name(
            "uk-h3").get_attribute("innerHTML")
        element_data["name"] = name

        details = element.find_elements_by_tag_name("li")
        for detail in details:
            p_tags = detail.find_elements_by_tag_name("p")
            raw_tags = []
            for p_tag in p_tags:
                text = p_tag.get_attribute("innerHTML")
                if(text.startswith(":")):
                    text = text[1:]
                raw_tags.append(text.strip())

            for i in range(len(raw_tags)):
                if i % 2 == 0:
                    element_data[raw_tags[i]] = raw_tags[i+1]

        result.append(element_data)

    return result


def reselection_after_submit_form(brand, model):
    wait_for_dropdown(driver.find_element_by_id("brands"))
    Select(driver.find_element_by_id("brands")).select_by_value(brand)

    wait_for_dropdown(driver.find_element_by_id("model"))
    Select(driver.find_element_by_id("model")).select_by_value(model)

    wait_for_dropdown(driver.find_element_by_id("altModel"))


def main():
    driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")
    find_button = driver.find_element_by_xpath(
        '//*[@id="find-battery"]/div[2]/button')

    years = driver.find_element_by_id("years")

    wait_for_dropdown(years)
    _year_options = years.find_elements_by_tag_name("option")

    year_options = []
    for year_option in _year_options:
        year_options.append(year_option.text)

    for year_option in year_options:
        _brand_options = selector("years", year_option, "brands")

        brand_options = []
        for brand_option in _brand_options:
            brand_options.append(brand_option.text)

        for brand_option in brand_options:
            _model_options = selector("brands", brand_option, "model")

            model_options = []
            for model_option in _model_options:
                model_options.append(model_option.text)

            for model_option in model_options:
                _submodel_options = selector(
                    "model", model_option, "altModel")

                submodel_options = []
                for submodel_option in _submodel_options:
                    submodel_options.append(submodel_option.text)

                for submodel_option in submodel_options:
                    submodel_selector = Select(
                        driver.find_element_by_id("altModel"))
                    submodel_selector.select_by_value(
                        submodel_option)

                    find_button = driver.find_element_by_xpath(
                        '//*[@id="find-battery"]/div[2]/button')
                    find_button.click()

                    get_items(
                        year_option, brand_option, model_option, submodel_option)

                    reselection_after_submit_form(
                        brand_option, model_option)

                    print("=====")


main()

# driver.close()
