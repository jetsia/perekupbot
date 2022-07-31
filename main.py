# Добавляем библиотеки
import requests
from bs4 import BeautifulSoup
import json


# Создаем функцию для получение новостей с сайта
def get_fist_news():
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }
# Делаем запрос на сайт
    url = 'https://www.kufar.by/l/r~minsk/mobilnye-telefony/mt~apple?sort=lst.d'
    r = requests.get(url=url, headers=headers)
# Парсим данные с помощью lxml с сайта и выбираем только карточки телефона
    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.select('div[data-name="listings"] > div > div > section > a')

# Создаем словарь для заполнения телефонами
    news_dist = {}
#  Проходимся циклом по карточке телефона и выбираем от туда Название телефона, цена, и где находится
    for article in articles_cards:
        article_title = article.find('h3').text.strip()
        article_desc = article.find('p').text.strip()
        # Выбираем ссылку и обрезаем сплитом оставляя только id
        article_url = article.get("href")
        article_id = article_url.split('/')[-1]

        # Заполняем словарь с помощью id, внутрь помещаем все данные
        news_dist[article_id] = {
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url
        }

    # Сохраним данные в JSON файл
    with open('news_dist.json', 'w') as file:
        # Передаем в файл news_dist - словарь с данными
        json.dump(news_dist, file, indent=3, ensure_ascii=False)

# Функция для проверки новых телефонов
def check_news_update():
    with open('news_dist.json') as file:
        news_dist = json.load(file)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
        }
        # Делаем запрос на сайт
        url = 'https://www.kufar.by/l/r~minsk/mobilnye-telefony/mt~apple?sort=lst.d'
        r = requests.get(url=url, headers=headers)
        # Парсим данные с помощью lxml с сайта и выбираем только карточки телефона
        soup = BeautifulSoup(r.text, 'lxml')
        articles_cards = soup.select('div[data-name="listings"] > div > div > section > a')

        # Создаем новый словарь для свежих новостей
        fresh_news = {}


        #Проходимся по карточкам телефонов и забираем id
        for article in articles_cards:
            article_url = article.get("href")
            article_id = article_url.split('/')[-1]
            # Условия проверки - Если id уже есть то телефон ничего не делаем
            if article_id in news_dist:
                continue
            # А если id нет добавляем новый телефон в файл
            else:
                article_title = article.find('h3').text.strip()
                article_desc = article.find('p').text.strip()

                # Добавляем новинку в словарь
                news_dist[article_id] = {
                    'article_title': article_title,
                    'article_desc': article_desc,
                    'article_url': article_url
                }

                fresh_news[article_id] = {
                    'article_title': article_title,
                    'article_desc': article_desc,
                    'article_url': article_url
                }

    with open('news_dist.json', 'w') as file:
        # Передаем в файл news_dist - словарь с данными
        json.dump(news_dist, file, indent=3, ensure_ascii=False)

    return fresh_news

# Функция main вызвывает функцию сбора телефонов

def main():
    # get_fist_news()
    print(check_news_update())

if __name__ == '__main__':
    main()

















