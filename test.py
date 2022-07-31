# url = 'https://www.kufar.by/item/154291809'
#
# article_id = url.split('/')[-1]
# print(article_id)
import json


with open('news_dist.json') as file:
    news_dist = json.load(file)

search_id = '152309285'

if search_id in news_dist:
    print('Телефон уже есть')
else:
    print('Новый телефон! добавляем')

