from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b0 = KeyboardButton('/Регистрация')

b1 = KeyboardButton('/Получить_задачи_ОГЭ')
b2 = KeyboardButton('/Доступная_теория')
b3 = KeyboardButton('/Полезные_ссылки')

b4 = KeyboardButton('/Выйти_из_тестирования')


kb_before_login = ReplyKeyboardMarkup(resize_keyboard=True).add(b0)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2).add(b3)


kb_client_testing = ReplyKeyboardMarkup(resize_keyboard=True).add(b4)

# insert(b3) - добавить кнопку справа, если есть место
# row(b1,b2,b3) - добавить кнопки в ряд