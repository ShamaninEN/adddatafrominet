import pymongo
from pymongo import MongoClient
import requests
from lxml import html
from pprint import pprint
import re
from datetime import datetime

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['geeekbrains']
collection_news = db['news']


main_link = "https://yandex.ru/news"
wanted_work = "Data Scientist"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
headers = {
    'User-Agent':user_agent
}
# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
# 2)Сложить все новости в БД
# params = {
#         "clusters": "true",
#         "enable_snippets": "true",
#         "salary": "",
#         "st": "searchVacancy",
#         "text": wanted_work,
#         "fromSearch": "true"
#         "page": page
#     }
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
blocks = dom.xpath("//h2[@class='story__title']")
date_now = datetime.now()
matched = 0
modified = 0
upserted = 0
for block in blocks:
    # pprint(block)
    news = {}
    link = block.xpath('.//a/@href')
    text = block.xpath('.//a/text()')
    link = re.sub(r"/news", main_link, link[0])
    news['link'] = link
    news['text'] = text[0]
    source_link = block.xpath('./parent::node()/following-sibling::node() //div[@class="story__date"]/text()')
    news['source_name'] = re.sub(r"\s\d{2}:\d{2}", '', source_link[0])
    date_full_str_source = re.search(r"\d{2}:\d{2}", source_link[0])
    date_full_str = re.findall(r"\d{2}", date_full_str_source[0])
    hour = int(date_full_str[0])
    minute = int(date_full_str[1])
    news['date'] = date_now.replace(hour=hour, minute=minute)
    pprint(news)
    result = collection_news.update_one(news, {'$set': {
        'link': news['link'],
        'text': news['text'],
        'date': news['date'],
        'source_name': news['source_name']
    }}, upsert=True)
    if result.matched_count != 0:
        matched += 1
    if result.modified_count != 0:
        modified += 1
    if result.upserted_id != None:
        upserted += 1
print(f'Finded: {matched} documents')
print(f'Modified: {modified} documents')
print(f'Added: {upserted} documents')