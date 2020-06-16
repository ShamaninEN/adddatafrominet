import pymongo
from pymongo import MongoClient
import requests
from lxml import html
from pprint import pprint
import re
from datetime import datetime

from update_news import update

def pars_mail(date_now):
    main_link = "https://news.mail.ru/"
    wanted_work = "Data Scientist"
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    blocks = dom.xpath("//div[contains(@name, 'clb')]//ul/li")
    news_list = []
    for block in blocks:
        news = {}
        link = block.xpath('.//a[@class="link link_flex"]/@href | .//a[@class="list__text"]/@href')
        text = block.xpath(
            './/a[@class="link link_flex"]/span[@class="link__text"]/text() | .//a[@class="list__text"]/text()')
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
        news['ad'] = 0
        news_list.append(update(news))
    return news_list


