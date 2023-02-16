from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from data_base.sqlite_db import sql_add_task, sql_read_all_tasks, sql_delete_command, sql_read_users
from keyboards.admin_kb import button_case_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None

class FSMAdmin(StatesGroup):
    """
    Машина состояний для создания новой записи в БД.
    """
    task_id = State()
    number_of_a_day = State()
    photo = State()
    right_answer = State()

# Начало диалога загрузки новой задачи
async def make_changes_comand(message:types.message):
    """
     Проверяем, что пользователь является админом
     при отправке пользователем комманды /moderator
     в групповой чат.
    """
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Данил, загрузи задачу', reply_markup=button_case_admin)
    await message.delete()

async def cm_start(message:types.message):
    """
    Запускаем машину сотояний, устанавливая курсор
    на первый параметр (или первую колонну будущей таблицы),
    т.е task_id.
    """
    if message.from_user.id == ID:
        await FSMAdmin.task_id.set()
        await message.reply('id задачи:')

#Выход из состояний
async def cancel_handler(message: types.message, state = FSMContext):
    """
    Выход из состояния, сброс введенных админом параметров.
    """
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

async def set_task_id(message: types.Message, state = FSMContext):
    """
    Ввод поля task_id, переход к состоянию set_a_day
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['task_id'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('На какую дату эта задача?')



# Ловим первый ответ и пишем в словарь
async def set_a_day(message:types.message, state: FSMContext):
    """
    Ввод поля set_a_day, переход к состоянию загрузки фото (load_photo)
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Пользователь вводит дату в формате день-месяц, год добавится автоматически (пока что 2023)
            data['number_of_a_day'] = f'2023-{str(message.text)}'
        await FSMAdmin.next()
        await message.reply('Загрузи фото')

# Загружаем фото задачи
async def load_photo(message:types.message, state: FSMContext):
    """
    Ввод поля photo (загружаем с устройства), причем в формате текста,
    т.е в БД попадает адрес фотографии.
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи ответ на задачу')


# Устанавливаем правильный ответ на задачу
async def set_right_answer(message:types.message, state: FSMContext):
    """
    Записываем правильный ответ на загруженную задачу,
    передаем все написанное в БД. Завершаем машину состояний.
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['right_answer'] = message.text

        await sql_add_task(state, 'oge_tasks')
        await state.finish()

async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена. ', show_alert=True)



async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_read_all_tasks()
        await bot.send_message(message.from_user.id, 'Задачи прочитаны')
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[2])
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))

async def get_all_users(message: types.message):
    users = await sql_read_users("*")
    await bot.send_message(message.from_user.id, f' Пользователи: {[*users]}')


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    """
    Регистрируем хэндлеры, функция регистрации хэндлерова выполняется
    в файле bot_telegram.py
    """
    dp.register_message_handler(make_changes_comand, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(set_task_id, state=FSMAdmin.task_id)
    dp.register_message_handler(set_a_day, state = FSMAdmin.number_of_a_day)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(set_right_answer, state=FSMAdmin.right_answer)
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(get_all_users, commands=['Посмотреть_пользователей'])
