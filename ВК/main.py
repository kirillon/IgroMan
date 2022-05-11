import os
import re
import urllib.request

from datetime import datetime

import requests
from typing import Tuple
from vkbottle.bot import Bot, Message
from config import TOKEN
from vkbottle import Keyboard, Text, PhotoMessageUploader, CtxStorage, BaseStateGroup, KeyboardButtonColor
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle import VKAPIError

bot = Bot(TOKEN)


def upload_inline_keyboard(keyboard, array):
    count = 0
    for item in array:
        if count % 3 == 0 and count != 0:
            keyboard.row()
        keyboard.add(Text(item))
        count += 1


# class в данном случае нужен для пошагового выполнения программы.
class Game(BaseStateGroup):
    TITLE = 0
    END = 1  # END я добавляю чтобы стейт останавливался.


def upload_keyboard(keyboard):  # загрузка клавиатуры
    button_1 = "/help"
    keyboard.add(Text(button_1), color=KeyboardButtonColor.POSITIVE)
    button_2 = "/top_2w"
    keyboard.add(Text(button_2), color=KeyboardButtonColor.PRIMARY)

    button_3 = "/top_f"
    keyboard.add(Text(button_3))
    button_4 = "/guess"
    keyboard.row()
    keyboard.add(Text(button_4), color=KeyboardButtonColor.NEGATIVE)
    button_5 = "/game"
    keyboard.add(Text(button_5), color=KeyboardButtonColor.PRIMARY)


@bot.on.message(text='/help')
async def help(message: Message):  # help хендлер
    await message.reply('''Что я умею:
    /top_2w - перечислю лучшие игры за последние две недели
    /top_f - перечислю топ игр за всё время
    /guess - помогу вспомнить игру
    /game - опишу игру''')


@bot.on.message(text="Начать")  # Start хендлер
async def start(message: Message):
    user = await bot.api.users.get(message.from_id)
    await message.reply(f'Привет, {user[0].first_name}! Меня зовут - Игроман. Я могу тебе подсказать во что тебе '
                        f'поиграть вечерком и сколько это грошей будет стоить. Чего тебе только еще надо, '
                        f'маленький еврейчик? ')
    keyboard = Keyboard()

    upload_keyboard(keyboard)
    await message.answer("Что ты хочешь спросить?", keyboard=keyboard)


@bot.on.message(text=['/top_2w'])  # топ за 2 недели хендлер
async def top_2w(message: Message):
    response = requests.get('https://igroman.herokuapp.com/api/v1/top2weeks')
    json_response = response.json()
    top = list()
    top1 = list()
    id_lst = []

    for i in range(len(json_response['data'])):
        top.append([json_response['data'][i]['title'],
                    str(int(json_response['data'][i]["price"]) / 100)
                    + "$", f" /id {json_response['data'][i]['steam_id']}"])
        id_lst.append(f"/id {json_response['data'][i]['steam_id']}")
        top1.append(", ".join(top[i]))

        top1[i] = f"{i + 1}. " + top1[i]
    keyboard = Keyboard(inline=True)
    upload_inline_keyboard(keyboard, id_lst)
    await message.reply("\n".join(top1), keyboard=keyboard)


@bot.on.message(CommandRule("id", ["/"], 1))  # поиск игры хендлер
async def search_game(message: Message, args: Tuple[int]):
    res = requests.get(f"https://igroman.herokuapp.com/api/v1/getGames/{args[0]}").json()
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

        suffix = datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join(["mylogfile", suffix]) + ".jpg"
        urllib.request.urlretrieve(poster, filename)

        photo_up = PhotoMessageUploader(bot.api)
        photo = await photo_up.upload(filename)
        os.remove(filename)

        await message.answer("", attachment=photo)
        await message.answer(f'''Название: {title}
    Жанр: {genre}
    Цена: {float(price) / 100} $
    Ссылка: {url}
    Описание: {description}''', )


@bot.on.private_message(text='/top_f')  # топ за все время хендлер
async def top_f(message: Message):
    response = requests.get('http://igroman.herokuapp.com/api/v1/topForeverGames/')
    json_response = response.json()
    id_lst = []
    top = list()
    top1 = list()
    for i in range(len(json_response['data'])):
        top.append([json_response['data'][i]['title'],
                    str(int(json_response['data'][i]["price"]) / 100)
                    + "$", f" /id{json_response['data'][i]['steam_id']}"])
        id_lst.append(f"/id {json_response['data'][i]['steam_id']}")
        top1.append(",".join(top[i]))
        top1[i] = f"{i + 1}. " + top1[i]
    keyboard = Keyboard(inline=True)
    upload_inline_keyboard(keyboard, id_lst)
    await message.reply("\n".join(top1), keyboard=keyboard)


@bot.on.private_message(text='/game')  # полная информация об игре хендлер
async def games(message: Message):
    await bot.state_dispenser.set(message.peer_id, Game.TITLE)
    return "Введите название игры"


@bot.on.private_message(state=Game.TITLE)  # поиска игры хендлер
async def search(message: Message):
    response = requests.get(f'https://igroman.herokuapp.com/api/v1/searchGames/?search={message.text}', timeout=5)
    jsone_response = response.json()
    id_lst = []
    top = list()
    top1 = list()
    for i in range(len(jsone_response['data'])):
        top.append([jsone_response['data'][i]['title'],
                    str(int(jsone_response['data'][i]["price"]) / 100)
                    + "$", f" /id{jsone_response['data'][i]['steam_id']}"])
        id_lst.append(f"/id {jsone_response['data'][i]['steam_id']}")
        top1.append(",".join(top[i]))
        top1[i] = f"{i + 1}. " + top1[i]
    try:
        keyboard = Keyboard(inline=True)
        upload_inline_keyboard(keyboard, id_lst)
        await message.reply(f"Найдено {len(jsone_response['data'])} результатов запроса\n" + "\n".join(top1),
                            keyboard=keyboard)
    except VKAPIError[911]:
        await message.reply("Извините, произошла ошибка. Мы не можем найти игру. Попробуйте написать от 5 символов ")


@bot.on.private_message()  # хендлер исключение
async def main(message):
    await message.reply(
        'Я не знаю, что ответить на это =(\n\nВозможно потом когда нибудь я смогу ответить тебе на это =)')


bot.run_forever()
