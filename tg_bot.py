import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from main import check_news_update
from config import token
import asyncio


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Привет, перекуп! Этот бот создан для мониторинга объявлений сайта kufar.by! Воспользоваться просто: Пиши команду /fresh_iphone и получай новые телефоны каждые 10 секунд!')


@dp.message_handler(commands='all_news')
async def get_all_news(message: types.Message):
    with open('news_dist.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f'{v["article_title"]}\n' \
               f'{v["article_desc"]}\n' \
               f'{v["article_url"]}'

        await message.answer(news)


@dp.message_handler(commands='last_five')
async def get_last_five_news(message: types.Message):
    with open('news_dist.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-1:]:
        news = f'{v["article_title"]}\n' \
               f'{v["article_desc"]}\n' \
               f'{v["article_url"]}'

        await message.answer(news)



@dp.message_handler(commands='fresh_iphone')
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        print('Да')
        await message.answer('Да')
        for k, v in fresh_news.items():
            news = f'{v["article_title"]}\n' \
                   f'{v["article_desc"]}\n' \
                   f'{v["article_url"]}\n'
            await message.answer(news)
            await message.answer('Да')
    else:
        await message.answer('Пока нет новых телефонов')



async def news_every_minute():
    while True:
        # user_id = 2056290693
        fresh_news = check_news_update()
        if len(fresh_news) >= 1:
            print('Да')
            for k, v in fresh_news.items():
                news = f'{v["article_title"]}\n' \
                       f'{v["article_desc"]}\n' \
                       f'{v["article_url"]}'
                await bot.send_message(2056290693, news)
        await asyncio.sleep(10)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)

