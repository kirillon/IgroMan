import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api

from Telegram_final import TOKEN, PATCHED_URL


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


setattr(api, "API_URL", PATCHED_URL)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await message.reply(text='''Привет! Меня зовут - Игроман.
    Ты можешь побольше узнать обо мне здесь: ??? ''', reply=False)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply(text='''Я знаю команды:
    /top - топ игр за месяц 
    /guess - помогу вспомнить игру
    /news - игровые новости''', reply=False)


def main():
    executor.start_polling(dispatcher=dp)


if __name__ == '__main__':
    main()
