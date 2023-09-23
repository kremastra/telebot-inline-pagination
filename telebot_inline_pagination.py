from math import ceil
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

current_page = 0

def text_callback(button_text_mode, current_page, text_index, callback_index, rows_per_page):
    keyboard = InlineKeyboardMarkup()
    for i in list_of_values[current_page*rows_per_page: current_page*rows_per_page+rows_per_page]:
        if button_text_mode == 1:
            button = InlineKeyboardButton(text=i[text_index], callback_data=i[callback_index])    
        elif button_text_mode == 2:
            button = InlineKeyboardButton(text=i[text_index] + ' (' + i[callback_index] + ')', callback_data=i[callback_index])               
        elif button_text_mode == 3:
            button = InlineKeyboardButton(text=i[callback_index] + ' (' + i[text_index] + ')', callback_data=i[callback_index])   
        else:
            button = InlineKeyboardButton(text=i[0], callback_data=i[0])
        keyboard.add(button)
    return keyboard

def send_keyboard(*, list_of_tuples, button_text_mode=None, text_index=0, callback_index=0, rows_per_page=5, next_page='--->'):
    
    global list_of_values, count, pages

    list_of_values = []    

    for i in list_of_tuples:
            list_of_values.append(i)

    count = len(list_of_values)
    pages = ceil(count/rows_per_page)              

    keyboard = text_callback(button_text_mode=button_text_mode, current_page=0, text_index=text_index, callback_index=callback_index, rows_per_page=rows_per_page)
    
    if pages > 1:
        keyboard.add(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(text=f'{1}/{pages}', callback_data=f'{1}/{pages}'),
                InlineKeyboardButton(text=next_page, callback_data='next_page')
                )
    else:
        keyboard.add(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(text=f'{1}/{pages}', callback_data=f'{1}/{pages}'),
                InlineKeyboardButton(text='-', callback_data='-')
                )   
    return keyboard

def edit_keyboard(call: CallbackQuery, *, button_text_mode=None, text_index=0, callback_index=0, rows_per_page=5, next_page='--->', previous_page='<---'): 
    
    global current_page
    
    if call.data == 'next_page' and current_page < pages:       
        current_page = current_page + 1
    elif call.data == 'previous_page' and current_page > 0:
        current_page = current_page - 1

    keyboard = text_callback(button_text_mode=button_text_mode, current_page=current_page, text_index=text_index, callback_index=callback_index, rows_per_page=rows_per_page)

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
   
