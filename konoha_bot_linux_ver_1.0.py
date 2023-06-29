import gspread as gspread
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import time

from telegram.bot import log

bot = telebot.TeleBot('put your token here')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('🇬🇧Английский', '🇯🇵Японский', '🇰🇷Корейский')
    bot.send_message(message.from_user.id,
                     "Привет! Этот бот поможет тебе записаться на пробное занятие в Коноху.\nКакой язык ты бы хотел(а) изучать?\n\nP.S. Если появилась проблема с записью (такое может случится при одновременной записи нескольких людей), то подожди, пожалуйста, 30 секунд и попробуй записаться еще раз. Спасибо за понимание 🌿",
                     reply_markup=user_markup)

def menu(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('🇬🇧Английский', '🇯🇵Японский', '🇰🇷Корейский')
    bot.send_message(message.from_user.id,
                     "Выбери пожалуйста язык",
                     reply_markup=user_markup)

@bot.message_handler(regexp='🇬🇧Английский')
def send_msg_eng(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    name_msg = bot.send_message(message.from_user.id, 'Как тебя зовут?', reply_markup=hide_markup)
    bot.register_next_step_handler(name_msg, user_name_eng)

def user_name_eng(message):
    name_surname = message.text
    if name_surname == '/menu':
        return menu(message)
    elif name_surname is None:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_eng)
    elif name_surname.isalpha() and len(name_surname) < 21:
        age_msg = bot.send_message(message.from_user.id, 'Сколько тебе лет?\n(Пиши только цифры)')
        bot.register_next_step_handler(age_msg, user_age_eng, name_surname)
    else:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_eng)

def user_age_eng(message, name_surname):
    age = message.text
    name_surnameE = name_surname
    if age == '/menu':
        return menu(message)
    elif age is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_eng, name_surnameE)
    elif age.isdigit() and int(age) < 107:
        level_msg = bot.send_message(message.from_user.id, 'Какой у тебя уровень языка?\nЕсли не знаешь, то просто напиши, что ты изучал(а)\n(Не больше 100 символов)')
        bot.register_next_step_handler(level_msg, user_level_eng, age, name_surnameE)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_eng, name_surnameE)

def user_level_eng(message, age, name_surname):
    level = message.text
    ageE = age
    name_surnameE = name_surname
    if level == '/menu':
        return menu(message)
    elif level is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_eng, ageE, name_surnameE)
    elif len(level) < 100:
        number_msg = bot.send_message(message.from_user.id, 'Укажи номер, по которому с тобой можно будет связаться(вместо +7 пиши 8)')
        bot.register_next_step_handler(number_msg, user_number_eng, ageE, name_surnameE, level)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Напиши пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_eng, ageE, name_surnameE)



def user_number_eng(message, age, name_surname, level):
    number = message.text
    ageE = age
    name_surnameE = name_surname
    levelE = level
    stre = str(number)
    if number == '/menu':
        return menu(message)
    elif len(stre) < 6:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_eng, ageE, name_surnameE, levelE)
    elif len(stre) > 17:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_eng, ageE, name_surnameE, levelE)
    elif (number is None):
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_eng, ageE, name_surnameE, levelE)
    elif number.isdigit():
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Позвонить', 'Написать')
        user_comm_msg = bot.send_message(message.from_user.id, 'Выбери, как лучше с тобой связаться', reply_markup=user_markup)
        bot.register_next_step_handler(user_comm_msg, user_comm_method_eng, ageE, name_surnameE, levelE, number)
    else:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_eng, ageE, name_surnameE, levelE)

def user_comm_method_eng(message, age, name_surname, level, number):
    comm_method = message.text
    ageE = age
    name_surnameE = name_surname
    levelE = level
    numberE = number
    if message.text == '/menu':
        return menu(message)
    elif comm_method is None:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_eng, ageE, name_surnameE, levelE, numberE)
    elif comm_method == 'Позвонить' or comm_method == 'Написать':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                   f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                   reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_eng, ageE, name_surnameE, levelE, numberE, comm_method)
    else:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_eng, ageE, name_surnameE, levelE, numberE)



def send_data_to_sheet_eng(message, age, name_surname, level, number, comm_method):
    if message.text == 'Да':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        add_to_gsheet(message, 'Английский', name_surname, age, level, number, comm_method)
        bot.send_message(message.from_user.id, 'Я тебя записал! Через некоторое время с тобой свяжутся для подтверждения записи на пробное занятие.', reply_markup=hide_markup)
    elif message.text is None:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_eng, age, name_surname, level, number, comm_method)
    elif message.text == 'Нет':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        fix = bot.send_message(message.from_user.id, 'Введи пожалуйста свои данные заново. Как тебя зовут?', reply_markup=hide_markup)
        bot.register_next_step_handler(fix, user_name_eng)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_eng, age, name_surname, level, number, comm_method)


@bot.message_handler(regexp='🇯🇵Японский')
def send_msg_jap(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    name_msg = bot.send_message(message.from_user.id, 'Как тебя зовут?', reply_markup=hide_markup)
    bot.register_next_step_handler(name_msg, user_name_jap)

def user_name_jap(message):
    name_surname = message.text
    if name_surname == '/menu':
        return menu(message)
    elif name_surname is None:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_jap)
    elif name_surname.isalpha() and len(name_surname) < 21:
        age_msg = bot.send_message(message.from_user.id, 'Сколько тебе лет?\n(Пиши только цифры)')
        bot.register_next_step_handler(age_msg, user_age_jap, name_surname)
    else:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_jap)

def user_age_jap(message, name_surname):
    age = message.text
    name_surnameJ = name_surname
    if age == '/menu':
        return menu(message)
    elif age is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_jap, name_surnameJ)
    elif age.isdigit() and int(age) < 107:
        level_msg = bot.send_message(message.from_user.id, 'Какой у тебя уровень языка?\nЕсли не знаешь, то просто напиши, что ты изучал(а)\n(Не больше 100 символов)')
        bot.register_next_step_handler(level_msg, user_level_jap, name_surnameJ, age)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_jap, name_surnameJ)

def user_level_jap(message, name_surname, age):
    level = message.text
    name_surnameJ = name_surname
    ageJ = age
    if level == '/menu':
        return menu(message)
    elif level is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Напиши пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_jap, name_surnameJ, ageJ)
    elif len(level) < 100:
        number_msg = bot.send_message(message.from_user.id, 'Укажи номер, по которому с тобой можно будет связаться(вместо +7 пиши 8)')
        bot.register_next_step_handler(number_msg, user_number_jap, name_surnameJ, ageJ, level)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Напиши пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_jap, name_surnameJ, ageJ)

def user_number_jap(message, name_surname, age, level):
    number = message.text
    name_surnameJ = name_surname
    ageJ = age
    levelJ = level
    stre = str(number)
    if number == '/menu':
        return menu(message)
    elif len(stre) < 6:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_jap, ageJ, name_surnameJ, levelJ)
    elif len(stre) > 17:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_jap, ageJ, name_surnameJ, levelJ)
    elif number is None:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_jap, name_surnameJ, ageJ, levelJ)
    elif number.isdigit():
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Позвонить', 'Написать')
        user_comm_msg = bot.send_message(message.from_user.id, 'Выбери, как лучше с тобой связаться', reply_markup=user_markup)
        bot.register_next_step_handler(user_comm_msg, user_comm_method_jap, name_surnameJ, ageJ, levelJ, number)
    else:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_jap, name_surnameJ, ageJ, levelJ)

def user_comm_method_jap(message, name_surname, age, level, number):
    comm_method = message.text
    name_surnameJ = name_surname
    ageJ = age
    levelJ = level
    numberJ = number
    if message.text == '/menu':
        return menu(message)
    elif comm_method is None:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_jap, name_surnameJ, ageJ, levelJ, numberJ)
    elif comm_method == 'Позвонить' or comm_method == 'Написать':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                   f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                   reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_jap, name_surnameJ, ageJ, levelJ, numberJ, comm_method)
    else:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_jap, name_surnameJ, ageJ, levelJ, numberJ)



def send_data_to_sheet_jap(message, name_surname, age, level, number, comm_method):
    if message.text == 'Да':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        add_to_gsheet(message, 'Японский', name_surname, age, level, number, comm_method)
        bot.send_message(message.from_user.id, 'Я тебя записал! Через некоторое время с тобой свяжутся для подтверждения записи на пробное занятие.', reply_markup=hide_markup)
    elif message.text is None:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_jap, name_surname, age, level, number, comm_method)
    elif message.text == 'Нет':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        fix = bot.send_message(message.from_user.id, 'Введи пожалуйста свои данные заново. Как тебя зовут?', reply_markup=hide_markup)
        bot.register_next_step_handler(fix, user_name_jap)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_jap, name_surname, age, level, number, comm_method)


@bot.message_handler(regexp='🇰🇷Корейский')
def send_msg_kor(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    name_msg = bot.send_message(message.from_user.id, 'Как тебя зовут?', reply_markup=hide_markup)
    bot.register_next_step_handler(name_msg, user_name_kor)

def user_name_kor(message):
    name_surname = message.text
    if name_surname == '/menu':
        return menu(message)
    elif name_surname is None:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_kor)
    elif name_surname.isalpha() and len(name_surname) < 21:
        age_msg = bot.send_message(message.from_user.id, 'Сколько тебе лет?\n(Пиши только цифры)')
        bot.register_next_step_handler(age_msg, user_age_kor, name_surname)
    else:
        age_error_msg = bot.send_message(message.from_user.id, 'Введи пожалуйста имя корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(age_error_msg, user_name_kor)

def user_age_kor(message, name_surname):
    age = message.text
    name_surnameK = name_surname
    if age == '/menu':
        return menu(message)
    elif age is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_kor, name_surnameK)
    elif age.isdigit() and int(age) < 107:
        level_msg = bot.send_message(message.from_user.id, 'Какой у тебя уровень языка?\nЕсли не знаешь, то просто напиши, что ты изучал(а)\n(Не больше 100 символов)')
        bot.register_next_step_handler(level_msg, user_level_kor, name_surnameK, age)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_age_kor, name_surnameK)

def user_level_kor(message, name_surname, age):
    level = message.text
    name_surnameK = name_surname
    ageK = age
    if level == '/menu':
        return menu(message)
    elif level is None:
        level_error_msg = bot.send_message(message.from_user.id, 'Напиши пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_kor, name_surnameK, ageK)
    elif len(level) < 100:
        number_msg = bot.send_message(message.from_user.id, 'Укажи номер, по которому с тобой можно будет связаться(вместо +7 пиши 8)')
        bot.register_next_step_handler(number_msg, user_number_kor, name_surnameK, ageK, level)
    else:
        level_error_msg = bot.send_message(message.from_user.id, 'Напиши пожалуйста уровень корректно. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(level_error_msg, user_level_kor, name_surnameK, ageK)

def user_number_kor(message, name_surname, age, level):
    number = message.text
    name_surnameK = name_surname
    ageK = age
    levelK = level
    stre = str(number)
    if number == '/menu':
        return menu(message)
    elif len(stre) < 6:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_kor, ageK, name_surnameK, levelK)
    elif len(stre) > 17:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_kor, ageK, name_surnameK, levelK)
    elif number is None:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_kor, name_surnameK, ageK, levelK)
    elif number.isdigit():
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Позвонить', 'Написать')
        user_comm_msg = bot.send_message(message.from_user.id, 'Выбери, как лучше с тобой связаться', reply_markup=user_markup)
        bot.register_next_step_handler(user_comm_msg, user_comm_method_kor, name_surnameK, ageK, levelK, number)
    else:
        user_comm_error_msg = bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(user_comm_error_msg, user_number_kor, name_surnameK, ageK, levelK)

def user_comm_method_kor(message, name_surname, age, level, number):
    comm_method = message.text
    name_surnameK = name_surname
    ageK = age
    levelK = level
    numberK = number
    if message.text == '/menu':
        return menu(message)
    elif comm_method is None:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_kor, name_surnameK, ageK, levelK, numberK)
    elif comm_method == 'Позвонить' or comm_method == 'Написать':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                   f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                   reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_kor, name_surnameK, ageK, levelK, numberK, comm_method)
    else:
        msg = bot.send_message(message.from_user.id, 'Выбери пожалуйста способ связи. Если ты хочешь выбрать другой язык, напиши/нажми /menu')
        bot.register_next_step_handler(msg, user_comm_method_kor, name_surnameK, ageK, levelK, numberK)



def send_data_to_sheet_kor(message, name_surname, age, level, number, comm_method):
    if message.text == 'Да':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        add_to_gsheet(message, 'Корейский', name_surname, age, level, number, comm_method)
        bot.send_message(message.from_user.id, 'Я тебя записал! Через некоторое время с тобой свяжутся для подтверждения записи на пробное занятие.', reply_markup=hide_markup)
    elif message.text is  None:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_kor, name_surname, age, level, number, comm_method)
    elif message.text == 'Нет':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        fix = bot.send_message(message.from_user.id, 'Введи пожалуйста свои данные заново. Как тебя зовут?', reply_markup=hide_markup)
        bot.register_next_step_handler(fix, user_name_kor)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Да', 'Нет')
        send_d = bot.send_message(message.from_user.id,
                                  f'Проверь, то, что ты указал(а): \nИмя: {name_surname} \nВозраст: {age} \nУровень языка: {level} \nТелефонный номер: {number} \nСпособ связи: {comm_method} \nВсё верно?',
                                  reply_markup=user_markup)
        bot.register_next_step_handler(send_d, send_data_to_sheet_kor, name_surname, age, level, number, comm_method)

# Google
gscope = []
gcredentials = 'path to json file'
gdocument = 'name of the google document'


now = datetime.now().date()
json_str = json.dumps(now, default=str)

def add_to_gsheet(message, lang, name_surname, age, level, number, comm_method):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
    gc = gspread.authorize(credentials)
    wks = gc.open(gdocument).sheet1
    wks.append_row([message.from_user.id, name_surname, age, lang, level, number, comm_method, json_str])

@bot.message_handler(content_types=['text','document', 'audio', 'video', 'photo', 'sticker', 'voice'])
def send_error(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Для того, чтобы записаться на пробное занятие напиши мне /start", reply_markup=hide_markup)



bot.polling(none_stop=True, skip_pending=True, interval=2)