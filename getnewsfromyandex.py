import pymongo
from pymongo import MongoClient
import requests
from lxml import html
from pprint import pprint
import re
from datetime import datetime
from update_news import update

def pars_yandex(date_now):
    main_link = "https://yandex.ru/news"
    wanted_work = "Data Scientist"
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    blocks = dom.xpath("//h2[@class='story__title']")
    news_list = []
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
        news['ad'] = 0
        news_list.append(update(news))

    return news_list