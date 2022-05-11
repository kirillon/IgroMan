import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api

from Telegram_final import TOKEN, PATCHED_URL
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests

import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class Games(StatesGroup):  # Класс для ожидания ответа
    title = State()


@dp.message_handler(commands=['start'])
async def hello(message: types.Message):  # Функция приветствия после команды /start
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="/help")  # Создание кнопок
    keyboard.add(button_1)
    button_2 = "/top_2w"
    keyboard.add(button_2)
    button_3 = "/top_f"
    keyboard.add(button_3)
    button_4 = "/game"
    keyboard.add(button_4)
    await message.reply(text='''Привет! Меня зовут - Игроман.
    Ты можешь побольше узнать обо мне здесь: ??? ''', reply=False)
    await message.answer("Что ты хочешь спросить?", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):  # Функция help
    await message.reply(text='''Что я умею:
    /top_2w - перечислю лучшие игры за последние две недели
    /top_f - перечислю топ игр за всё время
    /game - опишу игру''', reply=False)


@dp.message_handler(commands=['top_2w'])
async def top_2w(message: types.Message):  # Функция вывода топа за две недели
    response = requests.get('https://igroman.herokuapp.com/api/v1/top2weeks')  # Запрос на нашу API
    jsone_response = response.json()
    top = list()
    top1 = list()
    for i in range(len(jsone_response['data'])):  # Сортировка
        top.append([jsone_response['data'][i]['title'],
                    str(int(jsone_response['data'][i]["price"]) / 100)
                    + "$", f" /id{jsone_response['data'][i]['steam_id']}"])
        top1.append(",".join(top[i]))
        top1[i] = f"{i + 1}. " + top1[i]
    await message.reply(text="\n".join(top1), reply=False)  # Вывод


@dp.message_handler(commands=['top_f'])
async def top_f(message: types.Message):  # Функция топа за всё время(тоже самое, что и top_2w)
    response = requests.get('http://igroman.herokuapp.com/api/v1/topForeverGames/')
    jsone_response = response.json()
    top = list()
    top1 = list()
    for i in range(len(jsone_response['data'])):
        top.append([jsone_response['data'][i]['title'],
                    str(int(jsone_response['data'][i]["price"]) / 100)
                    + "$", f" /id{jsone_response['data'][i]['steam_id']}"])
        top1.append(",".join(top[i]))
        top1[i] = f"{i + 1}. " + top1[i]
    await message.reply(text="\n".join(top1), reply=False)


@dp.message_handler(commands=['game'])
async def game(message: types.Message):  # Функция описания игры по названию
    await message.reply(text="Введите название игры")
    await Games.title.set()


@dp.message_handler(state=Games.title)
async def search(message: types.Message, state: FSMContext):  # Функция рефлизующая /game
    async with state.proxy() as data:
        data['name'] = message.text
    response = requests.get(f'https://igroman.herokuapp.com/api/v1/searchGames/?search={message.text}',
                            timeout=5)  # Запрос
    json_response = response.json()

    top = list()  # Сортировка
    top1 = list()
    for i in range(len(json_response['data'])):
        top.append([json_response['data'][i]['title'],
                    str(int(json_response['data'][i]["price"]) / 100)
                    + "$", f" /id{json_response['data'][i]['steam_id']}"])

        top1.append(",".join(top[i]))
        top1[i] = f"{i + 1}. " + top1[i]

    await message.reply(
        f"Найдено {len(json_response['data'])} результатов запроса\n" + "\n".join(top1))  # Вызов функции massage
    await state.finish()  # Прекращение ожидания


@dp.message_handler(content_types=types.ContentType.ANY)
async def massage(message: types.Message):  # Функция вывода результата функции search
    if message.content_type == types.ContentType.TEXT:
        if "/id" in message.text:
            id = int(message.text[3:])
            res = requests.get(f"https://igroman.herokuapp.com/api/v1/getGames/{id}").json()
            if res["success"]:
                description = res["options"]["detailed_description"]
                title = res["data"]["title"]
                poster = res["options"]["header_image"]
                price = res["data"]["price"]
                genre = res["data"]["genre"]
                url = res["data"]["url"]
                print(description)
                description = re.sub(r'<[^>]*>', '', description)
                print(description)
                try:
                    await bot.send_photo(chat_id=message.chat.id, photo=f'{poster}')
                except:
                    pass

                await message.answer(f'''Название: {title}
Жанр: {genre}
Цена: {float(price) / 100} $
Ссылка: {url}
Описание: {description}''', parse_mode=types.ParseMode.HTML)
    else:
        pass


def main():
    executor.start_polling(dispatcher=dp)


if __name__ == '__main__':
    main()
