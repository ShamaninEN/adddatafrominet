import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
chrome_options = Options()
chrome_options.add_argument('start-fullscreen')
client = MongoClient('mongodb://localhost:27017/')
db = client['geeekbrains']
collection_mvideo = db['mvideo']
driver = webdriver.Chrome('/Users/evgeniyshamanin/gb_pars/chromedriver', options=chrome_options)

driver.get('https://mvideo.ru')

time.sleep(5)
button = driver.find_element_by_xpath("//div[contains(text(),'Хиты')]/parent::node()/parent::node()/following-sibling::node() //a[@class='next-btn sel-hits-button-next']")
actions = ActionChains(driver)
actions.move_to_element(button)
button.click()
time.sleep(1)
button.click()
time.sleep(1)
button.click()
time.sleep(1)
button.click()
actions.perform()

items = driver.find_elements_by_xpath("//div[contains(text(),'Хиты')]/parent::node()/parent::node()/following-sibling::node() //li[@class='gallery-list-item height-ready']")
for item in items:
    name = item.find_element_by_xpath(".//h4/a").get_attribute("data-product-info")

    b = json.loads(name)
    collection_mvideo.insert_one(b)
    print(b)
