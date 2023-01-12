from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Получить_задачи_ОГЭ')
b2 = KeyboardButton('/Доступная_теория')
b3 = KeyboardButton('/Полезные_ссылки')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3)
# insert(b3) - добавить кнопку справа, если есть место
# row(b1,b2,b3) - добавить кнопки в ряд