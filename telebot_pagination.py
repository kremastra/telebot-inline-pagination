from math import ceil
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

def start_button_pagination(*, list_of_tuples, rows_per_page=3, buttons_text_index=1, next_page='--->'):
    global buttons_text_data
    buttons_text_data = []

    for i in list_of_tuples:
        buttons_text_data.append(i[buttons_text_index])

    global count, pages, current_page
    current_page = 0
    count = len(buttons_text_data)
    pages = ceil(count/rows_per_page)    

    keyboard = InlineKeyboardMarkup()
    for i in buttons_text_data[current_page*rows_per_page: current_page*rows_per_page+rows_per_page]:
        button = InlineKeyboardButton(text=i, callback_data=i)
        keyboard.add(button)
    if pages > 1:
        keyboard.add(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(text=f'{current_page+1}/{pages}', callback_data=f'{current_page+1}/{pages}'),
                InlineKeyboardButton(text=next_page, callback_data='next_page')
                )
    else:
        keyboard.add(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(text=f'{current_page+1}/{pages}', callback_data=f'{current_page+1}/{pages}'),
                InlineKeyboardButton(text='-', callback_data='-')
                )   
    return keyboard

def edit_button_pagination(call: CallbackQuery, *, rows_per_page=3, next_page='--->', previous_page='<---'):
    global current_page
    if call.data == 'next_page' and current_page < pages:       
        current_page = current_page + 1
    elif call.data == 'previous_page' and current_page > 0:
        current_page = current_page - 1

    keyboard = InlineKeyboardMarkup()
    for i in buttons_text_data[current_page*rows_per_page: current_page*rows_per_page+rows_per_page]:
        button = InlineKeyboardButton(text=i, callback_data=i)
        keyboard.add(button)
    if current_page == 0:
        keyboard.add(
            InlineKeyboardButton(text='-', callback_data='-'),
            InlineKeyboardButton(text=f'{current_page+1}/{pages}', callback_data=f'{current_page+1}/{pages}'),
            InlineKeyboardButton(text=next_page, callback_data='next_page')
            )
    elif pages - current_page == 1:
        keyboard.add(
            InlineKeyboardButton(text=previous_page, callback_data='previous_page'),
            InlineKeyboardButton(text=f'{current_page+1}/{pages}', callback_data=f'{current_page+1}/{pages}'),
            InlineKeyboardButton(text='-', callback_data='-')
            )            
    else:
        keyboard.add(
            InlineKeyboardButton(text=previous_page, callback_data='previous_page'),
            InlineKeyboardButton(text=f'{current_page+1}/{pages}', callback_data=f'{current_page+1}/{pages}'),
            InlineKeyboardButton(text=next_page, callback_data='next_page')
            )      
    return keyboard      
   
