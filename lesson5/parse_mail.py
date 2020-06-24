from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
chrome_options = Options()
chrome_options.add_argument('start-fullscreen')

from pymongo import MongoClient
chrome_options = Options()
chrome_options.add_argument('start-fullscreen')
client = MongoClient('mongodb://localhost:27017/')
db = client['geeekbrains']
collection_mail = db['mail']

driver = webdriver.Chrome('/Users/evgeniyshamanin/gb_pars/chromedriver', options=chrome_options)

driver.get('https://mail.ru')

elem = driver.find_element_by_id('mailbox:login')

elem.send_keys('study.ai_172')
server_name = driver.find_element_by_id('mailbox:domain')
select = Select(server_name)
#
select.select_by_visible_text('@mail.ru')
#
#
server_name.submit()
#
elem = driver.find_element_by_id('mailbox:password')
elem = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID,'mailbox:password'))
)
#
elem.send_keys('NextPassword172')

server_name = driver.find_element_by_id('mailbox:submit')

server_name.submit()

time.sleep(5)
letter_link = driver.find_element_by_xpath("//div[@class='dataset-letters'] //a[contains(@class, 'js-tooltip-direction_letter-bottom')]")
letter_link.click()
time.sleep(5)


def letter_parse(driver):
    letter = {}
    letter['theme'] = driver.find_element_by_xpath("//h2[@class='thread__subject thread__subject_pony-mode']").text
    letter['author_mail'] = driver.find_element_by_xpath(
        "//div[@class='letter__author']/span[@class='letter-contact']").get_attribute('title')
    letter['author_name'] = driver.find_element_by_xpath(
        "//div[@class='letter__author']/span[@class='letter-contact']").get_attribute('title')
    letter['letter_time'] = driver.find_element_by_xpath("//div[@class='letter__date']").text
    letter['letter_body'] = driver.find_element_by_xpath("//div[@class='letter__body']").text
    collection_mail.insert_one(letter)
    return letter


print(letter_parse(driver))

i = True

while i:
    try:
        time.sleep(3)
        button = driver.find_element_by_xpath("//div[@class='portal-menu-element portal-menu-element_next portal-menu-element_expanded portal-menu-element_not-touch portal-menu-element_pony-mode']")
    except:
        i = False
    else:
        button.click()
        time.sleep(5)
        print(letter_parse(driver))
