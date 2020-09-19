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
    selection.select_by_value(selection_value.text)

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


def main():
    driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")
    find_button = driver.find_element_by_xpath(
        '//*[@id="find-battery"]/div[2]/button')

    years = driver.find_element_by_id("years")

    wait_for_dropdown(years)
    year_options = years.find_elements_by_tag_name("option")

    for year_option in year_options:
        the_year = year_option.text
        if the_year == "2018":
            brand_options = selector("years", year_option, "brands")
            for brand_option in brand_options:
                the_brand = brand_option.text
                if the_brand == "VOLKSWAGEN":
                    model_options = selector("brands", brand_option, "model")
                    for model_option in model_options:
                        the_model = model_option.text
                        if the_model == "PASSAT (3G2)":
                            submodel_options = selector(
                                "model", model_option, "altModel")
                            for submodel_option in submodel_options:
                                the_submodel = submodel_option.text
                                submodel_selector = Select(
                                    driver.find_element_by_id("altModel"))
                                submodel_selector.select_by_value(the_submodel)

                                find_button = driver.find_element_by_xpath(
                                    '//*[@id="find-battery"]/div[2]/button')
                                find_button.click()

                                get_items(
                                    the_year, the_brand, the_model, the_submodel)

                                wait_for_dropdown(
                                    driver.find_element_by_id("brands"))
                                Select(driver.find_element_by_id("brands")).select_by_value(
                                    the_brand)

                                wait_for_dropdown(
                                    driver.find_element_by_id("model"))
                                Select(driver.find_element_by_id("brands")).select_by_value(
                                    the_model)

                                wait_for_dropdown("altModel")

                                print(result)
                                print("=====")


main()

# driver.close()
