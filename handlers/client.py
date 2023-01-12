from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove

handlers_list = ['Получить_задачи_ОГЭ', 'Доступная_теория', 'Полезные_ссылки']
access_code = '6789'
users_list = []


# @dp.message_handler(commands= ['start', 'help'])
async def command_start(message: types.message):
    try:
        if message.text == '/start':
            if message.from_user.id not in users_list:
                await bot.send_message(message.from_user.id, 'Введите код доступа')
            else:
                await bot.send_message(message.from_user.id, 'И снова здравствуйте', reply_markup=kb_client)
        elif message.text == '/help':
            await bot.send_message(message.from_user.id, 'Помощь нужна?')
            await message.delete()
    except:
        await message.reply('Общение с ботом через лс, напишите ему')

async def get_access(message: types.message):
    if message.text == access_code:
        await message.reply('Все верно', reply_markup=kb_client)
        users_list.append(message.from_user.id)
    else:
        await message.reply('Неверно')

async def send_exercises(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Отправляю задачи...')
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через лс, напишите ему?')
        await message.delete()

async def send_theory(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Отправляю теорию...')
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через лс, напишите ему')
        await message.delete()

async def send_useful_links(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Отправляю полезные ссылки...')
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через лс, напишите ему')
        await message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(get_access)
    dp.register_message_handler(send_exercises, commands=[handlers_list[0]])
    dp.register_message_handler(send_theory, commands=[handlers_list[1]])
    dp.register_message_handler(send_useful_links, commands=[handlers_list[2]])