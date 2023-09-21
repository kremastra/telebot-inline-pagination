from api import bot
from telebot.types import CallbackQuery
from telebot_inline_pagination import start_inline_pagination, edit_inline_pagination
#from pandas import read_csv

#csv_airports = read_csv('D:/Work/Git/telebot-inline-pagination/book_airports.csv', sep=';', header=None)
#tuples_airports = csv_airports.values.tolist() 
#list_airports = [tuple(x) for x in tuples_airports] 

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

text_message = 'Демонстрация работы пагинатора'

@bot.message_handler(commands=['start'])
def demo_pagination(message):
    bot.send_message(message.from_user.id, text_message, reply_markup=start_inline_pagination(list_of_tuples = data, rows_per_page=3))

@bot.callback_query_handler(func=lambda call: True)
def demo_pagination_handler(call: CallbackQuery):
    if call.data in ('previous_page', 'next_page'):
        bot.edit_message_text(text_message, reply_markup = edit_inline_pagination(call, rows_per_page=3), chat_id = call.message.chat.id, message_id = call.message.message_id)
    for i in data:
        if call.data == i[1]:
            bot.send_message(
                        call.message.chat.id,
                        'Аэропорт: ' + i[0] + ' (' + i[1] + ')' + '\n' +
                        'Адрес: ' + i[2]
                        )
             
bot.infinity_polling()