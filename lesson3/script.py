import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
from datetime import datetime

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['geeekbrains']
collection_vacancy = db['vacancy']


main_link = "https://hh.ru/search/vacancy"
wanted_work = "Data Scientist"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
headers = {
    'User-Agent':user_agent
}
# функция выдергивания зарплаты из объявления
def find_salary(some_str):
    return_salary = {
        'salary min': None,
        'salary max': None,
        'currency': None
    }
    if some_str[0] == 'о':
        salary_min = re.findall(r"\d", some_str)
        currency = re.findall(r"\w*\S$", some_str)
        return_salary['salary min'] = int(''.join(salary_min))
        return_salary['currency'] = currency[0]
        return return_salary
    elif some_str[0] == 'д':
        salary_max = re.findall(r"\d", some_str)
        currency = re.findall(r"\w*\S$", some_str)
        return_salary['salary max'] = int(''.join(salary_max))
        return_salary['currency'] = currency[0]
        return return_salary
    else:
        index_tire = some_str.index('-')
        first_path = some_str[0:index_tire]
        second_path = some_str[index_tire:len(some_str)]
        salary_min = re.findall(r"\d", first_path)
        return_salary['salary min'] = int(''.join(salary_min))
        salary_max = re.findall(r"\d", second_path)
        return_salary['salary max'] = int(''.join(salary_max))
        currency = re.findall(r"\w*\S$", second_path)
        return_salary['currency'] = currency[0]
        return return_salary
page = 0
i = True
matched = 0
modified = 0
upserted = 0
# устанавливаем дату обновления
date_now = datetime.now()
while i == True:
    params = {
        "clusters": "true",
        "enable_snippets": "true",
        "salary": "",
        "st": "searchVacancy",
        "text": wanted_work,
        "fromSearch": "true",
        "page": page
    }
    response = requests.get(main_link, params=params, headers=headers)
    soup = bs(response.text, 'lxml')
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    try:
        page_link = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
    except TypeError:
        i = False
    else:
        page = page_link[len(page_link)-1]
    for work in vacancy_list:
        vacansy = {
        'site': None,
        'link':None,
        'vacancy_name':None,
        'salary': {
            'salary min': None,
            'salary max': None,
            'currency': None
        }
    }
        site = re.findall(r"https:\/\/\S*\.\S{2,3}",main_link)
        vacansy['site'] = site[0]
        vacansy['link'] = work.find('a',{'class':'bloko-link HH-LinkModifier'})['href']
        vacansy['vacancy_name'] = work.find('a',{'class':'bloko-link HH-LinkModifier'}).text
        salary = work.find('div', {'class':'vacancy-serp-item__sidebar'}).text
        if len(salary) != 0:
            vacansy['salary'] = find_salary(salary)
        # обновляем вакансии, если такой нету то добавляем
        result = collection_vacancy.update_one(vacansy, {'$set':{
            'site': vacansy['site'],
            'link': vacansy['link'],
            'vacancy_name':vacansy['vacancy_name'],
            'salary': {
                'salary min': vacansy['salary']['salary min'],
                'salary max': vacansy['salary']['salary max'],
                'currency': vacansy['salary']['currency']
            },
            'date': date_now
        }}, upsert=True)
        if result.matched_count != 0:
            matched +=1
        if result.modified_count != 0:
            modified +=1
        if result.upserted_id != None:
            upserted +=1
        # vacancy_array.append(vacansy)
    # pprint(vacancy_array)
# for work in collection_vacancy.find({}):
#     pprint(work)
print(f'Finded: {matched} documents')
print(f'Modified: {modified} documents')
print(f'Added: {upserted} documents')
# удаляем те вакансии которых нет на сайте
result = db.collection_vacancy.delete_many({"date": {"$lte": date_now}})
print(f'Удаленных вакансий: {result.deleted_count}')