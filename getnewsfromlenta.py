import requests
from lxml import html
from pprint import pprint
import re

from update_news import update

def pars_lenta(date_now):
    main_link = "https://lenta.ru/"
    wanted_work = "Data Scientist"
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    blocks = dom.xpath(
        "//a/time[@class='g-time']/parent::node() | //span[contains(@class,'g-date')]/span[@class='time']")

    news_list = []
    for block in blocks:
        # pprint(block)
        news = {}

        if len(block.xpath('.//@href')) > 0:
            link = block.xpath('.//@href')
            news['link'] = re.sub(r"^/", main_link, link[0])

            text = block.xpath('.//text()')
            news['text'] = ' '.join(text[1:len(text)])

            date_full_str_source = re.search(r"^\d{2}:\d{2}", text[0])
            date_full_str = re.findall(r"\d{2}", date_full_str_source[0])
            hour = int(date_full_str[0])
            minute = int(date_full_str[1])
            news['date'] = date_now.replace(hour=hour, minute=minute)
            source_name = re.search(r'lenta.ru', news['link'])
            try:
                news['source_name'] = source_name.group(0)
            except AttributeError:
                news['source_name'] = 'None'
                # скрытая реклама
            result = re.match(r'https://lenta.ru/', news['link'])
            if result == None:
                news['ad'] = 1
            else:
                news['ad'] = 0
            # pprint(link)
            # pprint(update(news))
            # вернем результат обновления
            news_list.append(update(news))

        else:
            link = block.xpath('.//parent::node()/parent::node()/following-sibling::node() //a/@href')
            text = block.xpath('.//parent::node()/parent::node()/following-sibling::node() //a/span/text()')
            date_full_str_source = block.xpath('./text()')
            date_full_str = re.findall(r"\d{2}", date_full_str_source[0])
            news['link'] = re.sub(r"^/", main_link, link[0])
            news['text'] = text[0]
            # скрытая реклама
            result = re.match(r'https://lenta.ru/', news['link'])
            if result == None:
                news['ad'] = 1
            else:
                news['ad'] = 0
            hour = int(date_full_str[0])
            minute = int(date_full_str[1])
            news['date'] = date_now.replace(hour=hour, minute=minute)
            source_name = re.search(r'lenta.ru', news['link'])
            try:
                news['source_name'] = source_name.group(0)
            except AttributeError:
                news['source_name'] = 'None'
            news_list.append(update(news))

    return news_list


