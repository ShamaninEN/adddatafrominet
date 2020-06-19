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

# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# * от кого,
# * дата отправки,
# * тема письма,
# * текст письма полный
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172
# 3) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

driver = webdriver.Chrome('/Users/evgeniyshamanin/gb_pars/chromedriver', options=chrome_options)
# driver.manage().window().maximize()
driver.get('https://mail.ru')
elem = driver.find_element_by_id('mailbox:login')
# elem.send_keys('region-ctroy')
elem.send_keys('study.ai_172')
server_name = driver.find_element_by_id('mailbox:domain')
select = Select(server_name)
# select.select_by_visible_text('@bk.ru')
select.select_by_visible_text('@mail.ru')


server_name.submit()

elem = driver.find_element_by_id('mailbox:password')
elem = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID,'mailbox:password'))
)
# elem.send_keys('89000962124regionCtroy')
elem.send_keys('NextPassword172')

server_name = driver.find_element_by_id('mailbox:submit')

# зависает в загрузке пришлось перезагружать окно
server_name.submit()
time.sleep(2)
driver.refresh()
time.sleep(10)
# driver.send_keys(Keys.END)
# time.sleep(15)
links = driver.find_elements_by_xpath('//a[contains(@href, "/inbox/0")]')
for link in links:
    print(link.get_attribute('href'))
for i in range(5):
    time.sleep(5)
    articles = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located(links))
    actions = ActionChains(driver)
    actions.move_to_element(links[-1])
    actions.perform()

# link = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.CLASS_NAME,'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal'))
# )
# print(link.get_attribute('href'))

# time.sleep(15)
# driver.get('https://e.mail.ru/inbox/')
# elem = WebDriverWait(driver, 15).until(
#     EC.element_to_be_clickable((By.ID,'0:15924712301346674112:0'))
# )
# elem = driver.find_element_by_id('0:15924712301346674112:0')
# print(elem.get_attribute('href'))


# for link in links:
#     print(link)