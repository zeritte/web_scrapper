from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.inciaku.com/tr/akunu-bul/otomobil-hafif-ticari")

years = driver.find_element_by_id("years")

time.sleep(10)
print(len(years.find_elements_by_tag_name('option')))
# for option in years.find_elements_by_tag_name('option'):
#     print(option.text)
