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

elem.send_keys('study.ai_172')
server_name = driver.find_element_by_id('mailbox:domain')
select = Select(server_name)

select.select_by_visible_text('@mail.ru')


server_name.submit()

elem = driver.find_element_by_id('mailbox:password')
elem = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID,'mailbox:password'))
)

elem.send_keys('NextPassword172')

server_name = driver.find_element_by_id('mailbox:submit')

# зависает в загрузке пришлось перезагружать окно
server_name.submit()
time.sleep(2)
driver.refresh()
time.sleep(5)

def show_links():
    links = driver.find_elements_by_xpath('//a[contains(@href, "/inbox/0")]')

    last_letter = links[-1]
    print(last_letter)
    for link in links:
        print(link.get_attribute('href'))
    return last_letter

show_links()
i = 0
while True:
    i +=1
    articles = driver.find_elements_by_xpath('//a[contains(@href, "/inbox/0")]')
    actions = ActionChains(driver)
    actions.move_to_element(show_links())
    time.sleep(1)
    actions.perform()
