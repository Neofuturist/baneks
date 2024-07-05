# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import http.client
from random import randrange
import telebot
from telebot import types

bot = telebot.TeleBot('7129810701:AAEmpkOutHO5t3d6qOmvA3i4ZtGcI2aMWTw')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Случайный анек")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Нажми на кнопку, чтобы прочитать анек. \nВведи номер анека, чтобы прочитать его.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Случайный анек':
        anek = get_anek()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Случайный анек")
        markup.add(btn1)
        bot.send_message(message.from_user.id, anek, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
    elif message.text.isdigit():
        if (int(message.text) >= 1 <= 1142):
            anek = get_anek(message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Случайный анек")
            markup.add(btn1)
            bot.send_message(message.from_user.id, anek, parse_mode='Markdown', disable_web_page_preview=True,
                             reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Случайный анек")
            markup.add(btn1)
            bot.send_message(message.from_user.id,
                             "Нет такого анека!",
                             reply_markup=markup)
    else:
        start(message)


def get_anek(number=None):
    conn = http.client.HTTPSConnection("baneks.ru")
    anekId = randrange(1, 1142)
    if number:
        anekId = int(number)
    conn.request("GET", "/" + str(anekId))
    response = conn.getresponse()
    print(response.status, response.reason)
    response_str = response.read().decode("utf-8")
    end_number = "Анекдот [#" + str(anekId) + "](baneks.ru/" + str(anekId) + ")"
    print("number: " + end_number)
    start_anek = str(response_str[response_str.find("<meta name=\"description\" content=\"") + 34: len(response_str)])
    end_anek = start_anek.split("\">")[0]
    print("anek: " + end_anek)
    conn.close()
    return end_number + "\n\n" + end_anek


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
