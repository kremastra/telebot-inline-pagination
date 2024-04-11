from api import bot # Telegram Token
from telebot.types import CallbackQuery
from telebot_inline_pagination import Keyboard

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

BUTTON_TEXT_MODE = 2
TEXT_INDEX = 0
CALLBACK_INDEX = 1
ROW_WIDTH = 1
ROWS_PER_PAGE = 3
NEXT_PAGE = '>'
PREVIOUS_PAGE = '<'

keyboards = []

@bot.message_handler(commands=['start'])
def demo_pagination(message):
    for i, j in enumerate(keyboards):
        if j["id"] == message.chat.id:
            del keyboards[i]
    json = {"id": message.chat.id, "object": Keyboard(chat_id=message.chat.id, data=data, row_width=ROW_WIDTH, rows_per_page=ROWS_PER_PAGE, button_text_mode=BUTTON_TEXT_MODE, text_index=TEXT_INDEX, callback_index=CALLBACK_INDEX, next_page=NEXT_PAGE, previous_page=PREVIOUS_PAGE)}
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
        if call.data == i[CALLBACK_INDEX]:
            bot.send_message(
                        call.message.chat.id,
                        'Airport: ' + i[0] + ' (' + i[1] + ')' + '\n' +
                        'Address: ' + i[2]
                        )

bot.infinity_polling()