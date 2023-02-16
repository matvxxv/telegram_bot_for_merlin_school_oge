from sqlite3 import IntegrityError

from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards.client_kb import kb_client, kb_before_login
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline_client_btns import create_urlkb
from data_base.sqlite_db import sql_add_user, sql_read_users

handlers_list = ['Получить_задачи_ОГЭ', 'Доступная_теория', 'Полезные_ссылки']



async def command_start(message: types.Message):
    try:
        if message.text == '/start':
            users = await sql_read_users("user_id")
            if (str(message.from_user.id),) not in users:
                await bot.send_message(message.from_user.id, 'Нажми /Регистрация перед использованием бота.', reply_markup=kb_before_login)
            else:
                await bot.send_message(message.from_user.id, 'И снова здравствуйте', reply_markup=kb_client)
        elif message.text == '/help':
            await bot.send_message(message.from_user.id, 'Помощь нужна?')
            await message.delete()
    except:
        await message.reply('Общение с ботом через лс, напишите ему')

async def authoriztion(message:types.message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username
        full_name = message.from_user.full_name
        data = {
            'user_id': user_id,
            'username': username,
            'full_name': full_name
        }
        await sql_add_user(data)
        await bot.send_message(message.from_user.id, 'Вы успешно зарегистрированны!', reply_markup=kb_client)
    except IntegrityError:
        await message.reply('Вы уже зарегистрированны', reply_markup=kb_client)


async def send_theory(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Отправляю теорию...')
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через лс, напишите ему')
        await message.delete()

async def send_useful_links(message: types.Message):
    try:
        urlkb = await create_urlkb()
        await bot.send_message(message.from_user.id, 'Полезные ссылки: \n \n', reply_markup=urlkb)
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через лс, напишите ему')
        await message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(authoriztion, commands=['Регистрация'])
    dp.register_message_handler(send_theory, commands=[handlers_list[1]])
    dp.register_message_handler(send_useful_links, commands=[handlers_list[2]])
