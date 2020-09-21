# coding=utf-8


import time
from openpyxl import Workbook, load_workbook
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)


wb = load_workbook(filename='Results_Existing.xlsx')
ws = wb.active


def save_to_excel(that_row):
    ws.append(list(that_row.values()))
    wb.save("Results_New.xlsx")


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
            save_to_excel(element_data)

    except Exception as e:
        print(str(e))


def reselection_after_submit_form(brand, model):
    wait_for_dropdown(driver.find_element_by_id("brands"))
    Select(driver.find_element_by_id("brands")).select_by_value(brand)

    wait_for_dropdown(driver.find_element_by_id("model"))
    Select(driver.find_element_by_id("model")).select_by_value(model)

    wait_for_dropdown(driver.find_element_by_id("altModel"))


def main():
    year_options = ['1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

    # year_options.reverse()
    for year_option in year_options[14:]:
        print("YIL", year_option)

        driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")
        wait_for_dropdown(driver.find_element_by_id("years"))

        _brand_options = selector("years", year_option, "brands")

        brand_options = []
        for brand_option in _brand_options:
            brand_options.append(brand_option.text)

        # remove
        print(">>>>>>>>>>")
        print(brand_options)
        print("<<<<<<<<<<")
        # remove

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
