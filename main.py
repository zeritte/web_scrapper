# coding=utf-8

import time
from openpyxl import Workbook
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)


wb = Workbook()
ws = wb.active

columns = ["Name", "Recommended", "Type", "Year", "Brand", "Model", "Submodel", "Akü Kodu",
           "Volt (V)", "Kapasite", "CCA", "En", "Boy", "Yükseklik", "Alt Bağlantı Tipi", "Terminal Tipi", "URL"]

ws.append(columns)
wb.save("Results.xlsx")


result = []


def load_to_excel(that_row):
    arr = []
    for key, value in that_row.items():
        arr.append(value)
    ws.append(arr)
    wb.save("Results.xlsx")


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
    print(year_option, brand_option, model_option, submodel_option)
    try:
        parent_element = driver.find_element_by_xpath(
            "/html/body/section/div[4]/div")
        element_list = parent_element.find_elements_by_tag_name("a")

        for element in element_list:
            element_data = {}

            name = element.find_element_by_class_name(
                "uk-h3").get_attribute("innerHTML")
            element_data["Name"] = name

            recommended = element.find_element_by_class_name("uk-text-bolder")
            if recommended.get_attribute("innerHTML").startswith("TAVS"):
                recommended = "TAVSIYE EDILEN"
            else:
                recommended = recommended.get_attribute("innerHTML")
            element_data["Recommended"] = recommended

            type_of = element.find_element_by_class_name(
                "uk-text-small").get_attribute("innerHTML")
            element_data["Type"] = type_of

            print("******")
            print(type_of)
            print("******")

            element_data["Year"] = year_option
            element_data["Brand"] = brand_option
            element_data["Model"] = model_option
            element_data["Submodel"] = submodel_option

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

            element_data["URL"] = driver.current_url
            load_to_excel(element_data)
            result.append(element_data)

    except Exception as e:
        print(str(e))


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
    for year_option in _year_options[1:]:
        year_options.append(year_option.text)

    for year_option in year_options:
        print("YIL", year_option)
        _brand_options = selector("years", year_option, "brands")

        brand_options = []
        for brand_option in _brand_options:
            brand_options.append(brand_option.text)

        for brand_option in brand_options:
            print("MARKA", brand_option)
            _model_options = selector("brands", brand_option, "model")

            model_options = []
            for model_option in _model_options:
                model_options.append(model_option.text)

            for model_option in model_options:
                print("MODEL", model_option)
                _submodel_options = selector(
                    "model", model_option, "altModel")

                submodel_options = []
                for submodel_option in _submodel_options:
                    submodel_options.append(submodel_option.text)

                for submodel_option in submodel_options:
                    print("ALTMODEL", submodel_option)
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

driver.close()
