from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
chrome_options = Options()
chrome_options.add_argument('start-fullscreen')

driver = webdriver.Chrome('/Users/evgeniyshamanin/gb_pars/chromedriver', options=chrome_options)

driver.get('https://mvideo.ru')
# time.sleep(5)
# a = driver.find_element_by_class_name('btn btn-approve-city')

button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(driver.find_element_by_class_name('btn btn-approve-city'))
)
button.click()

# list = driver.find_elements_by_class_name('gallery-list-item height-ready')
# for elem in list:
#     print(elem.get_attribute())