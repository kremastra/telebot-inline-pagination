"""Pageable inline keyboard for pyTelegramBotAPI.

A library for pyTelegramBotAPI that allows you to display data in the format of a pageable inline keyboard.
"""

from math import ceil
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

class Keyboard():
    """Pageable inline keyboard which contain inline buttons."""

    def __init__(self, chat_id: int, data: list, rows_per_page=5, button_text_mode=0, text_index=0, callback_index=0, next_page='--->', previous_page='<---'):
        """Construct a pageable inline keyboard."""        
        self.chat_id = chat_id
        self.current_page = 0
        self.data = data
        self.count = len(self.data)
        self.pages = ceil(self.count/rows_per_page)
        self.rows_per_page = rows_per_page
        self.button_text_mode = button_text_mode
        self.text_index = text_index
        self.callback_index = callback_index
        self.next_page = next_page
        self.previous_page = previous_page

    def text_callback(self):
        keyboard = InlineKeyboardMarkup()
        for i in self.data[self.current_page*self.rows_per_page: self.current_page*self.rows_per_page+self.rows_per_page]:
            if self.button_text_mode == 1:
                button = InlineKeyboardButton(text=i[self.text_index], callback_data=i[self.callback_index])    
            elif self.button_text_mode == 2:
                button = InlineKeyboardButton(text=i[self.text_index] + ' (' + i[self.callback_index] + ')', callback_data=i[self.callback_index])               
            elif self.button_text_mode == 3:
                button = InlineKeyboardButton(text=i[self.callback_index] + ' (' + i[self.text_index] + ')', callback_data=i[self.callback_index])   
            else:
                button = InlineKeyboardButton(text=i[0], callback_data=i[0])
            keyboard.add(button)
        return keyboard

    def send_keyboard(self):
        """Return first page of the inline keyboard."""       
        keyboard = self.text_callback()      
        if self.pages > 1:
            keyboard.add(
                    InlineKeyboardButton(text='-', callback_data='-'),
                    InlineKeyboardButton(text=f'{1}/{self.pages}', callback_data=f'{1}/{self.pages}'),
                    InlineKeyboardButton(text=self.next_page, callback_data='next_page')
                    )
        return keyboard

    def edit_keyboard(self, call: CallbackQuery):
        """Navigate between pages using the 'next page' and 'previous page' buttons."""        
        if call.data == 'next_page' and self.current_page < self.pages:       
            self.current_page = self.current_page + 1
        elif call.data == 'previous_page' and self.current_page > 0:
            self.current_page = self.current_page - 1

        keyboard = self.text_callback()

        if self.current_page == 0:
            keyboard.add(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(text=f'{self.current_page+1}/{self.pages}', callback_data=f'{self.current_page+1}/{self.pages}'),
                InlineKeyboardButton(text=self.next_page, callback_data='next_page')
                )
        elif self.pages - self.current_page == 1:
            keyboard.add(
                InlineKeyboardButton(text=self.previous_page, callback_data='previous_page'),
                InlineKeyboardButton(text=f'{self.current_page+1}/{self.pages}', callback_data=f'{self.current_page+1}/{self.pages}'),
                InlineKeyboardButton(text='-', callback_data='-')
                )            
        else:
            keyboard.add(
                InlineKeyboardButton(text=self.previous_page, callback_data='previous_page'),
                InlineKeyboardButton(text=f'{self.current_page+1}/{self.pages}', callback_data=f'{self.current_page+1}/{self.pages}'),
                InlineKeyboardButton(text=self.next_page, callback_data='next_page')
                )      
        return keyboard      
   
