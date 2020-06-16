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


main_link = "https://news.mail.ru/"
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
blocks = dom.xpath("//div[contains(@name, 'clb')]//ul/li")

matched = 0
modified = 0
upserted = 0
for block in blocks:
    news = {}
    link = block.xpath('.//a[@class="link link_flex"]/@href | .//a[@class="list__text"]/@href')
    text = block.xpath('.//a[@class="link link_flex"]/span[@class="link__text"]/text() | .//a[@class="list__text"]/text()')
    link = re.sub(r"^/", main_link, link[0])
    news['link'] = link
    news['text'] = text[0]
    response_news = requests.get(link, headers=headers)
    dom_news = html.fromstring(response_news.text)
    blocks_news = dom_news.xpath("//div[@class='breadcrumbs breadcrumbs_article js-ago-wrapper']")
    for block_news in blocks_news:
        time_news = block_news.xpath('.//span[@datetime]/@datetime')
        news['date'] = datetime.fromisoformat(time_news[0])
        # pprint(time_news)
        source_news_link = block_news.xpath('.//a[@class="link color_gray breadcrumbs__link"]/@href')
        source_news_text = block_news.xpath('.//a[@class="link color_gray breadcrumbs__link"]/span/text()')
        news['source_link'] = source_news_link[0]
        # pprint(source_news_link)
        news['source_name'] = source_news_text[0]
        # pprint(source_news_text)
    # pprint(link)
    pprint(news)
    result = collection_news.update_one(news, {'$set': {
        'link': news['link'],
        'text': news['text'],
        'date': news['date'],
        'source_link': news['source_link'],
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