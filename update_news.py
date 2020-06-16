from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client['geeekbrains']
collection_news = db['news']

date_now = datetime.now()

def update(news):
    responce = {
        'matched': 0,
        'modified': 0,
        'upserted': 0
    }
    result = collection_news.update_one(news, {'$set': {
        'link': news['link'],
        'text': news['text'],
        'date': news['date'],
        'ad': news['ad'],
        'source_name': news['source_name'],
        'updated': date_now
    }}, upsert=True)
    if result.matched_count != 0:
        responce['matched'] += 1
    if result.modified_count != 0:
        responce['modified'] += 1
    if result.upserted_id != None:
        responce['upserted'] += 1

    return responce


