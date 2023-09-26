from api import bot # Telegram Token
from telebot.types import CallbackQuery
from telebot_inline_pagination.keyboard import Keyboard

data = [
            ('Hartsfield-Jackson Atlanta International Airport', 'ATL/KATL', 'Atlanta, Georgia, United States'),
            ("O'Hare International Airport", 'ORD/KORD', 'Chicago, Illinois, United States'),
            ('Dallas/Fort Worth International Airport', 'DFW/KDFW', 'Coppell, Euless, Grapevine, and Irving, Texas, United States'),
            ('Denver International Airport', 'DEN/KDEN', 'Denver, Colorado, United States'),
            ('Charlotte Douglas International Airport', 'CLT/KCLT', 'Charlotte, North Carolina, United States'),
            ('Los Angeles International Airport', 'LAX/KLAX', 'Los Angeles, California, United States'),
            ('Harry Reid International Airport', 'LAS/KLAS', 'Paradise, Nevada, United States'),
            ('Phoenix International Airport', 'PHX/KPHX', 'Phoenix, Arizona, United States'),
            ('Miami International Airport', 'MIA/KMIA', 'Miami-Dade County, Florida, United States'),
            ('George Bush Intercontinental Airport', 'IAH/KIAH', 'Houston, Texas, United States')
        ]

text_message = 'Demo'

button_text_mode = 2
text_index = 0
callback_index = 1
rows_per_page = 3
next_page = '>'
previous_page = '<'

keyboards = []

@bot.message_handler(commands=['start'])
def demo_pagination(message):
    for i, j in enumerate(keyboards):
        if j["id"] == message.chat.id:
            del keyboards[i]
    json = {"id": message.chat.id, "object": Keyboard(chat_id=message.chat.id, data=data, rows_per_page=rows_per_page, button_text_mode=button_text_mode, text_index=text_index, callback_index=callback_index, next_page=next_page, previous_page=previous_page)}
    keyboards.append(json)
    for i in keyboards:
        if i["id"] == message.chat.id:
            bot.send_message(message.from_user.id, text_message, reply_markup=i["object"].send_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def demo_pagination_handler(call: CallbackQuery):
    if call.data in ('previous_page', 'next_page'):
        for i in keyboards:
            if i["id"] == call.message.chat.id:
                bot.edit_message_text(text_message, reply_markup = i["object"].edit_keyboard(call), chat_id = call.message.chat.id, message_id = call.message.message_id)
    for i in data:
        if call.data == i[callback_index]:
            bot.send_message(
                        call.message.chat.id,
                        'Airport: ' + i[0] + ' (' + i[1] + ')' + '\n' +
                        'Address: ' + i[2]
                        )

bot.infinity_polling()