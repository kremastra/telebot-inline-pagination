"""
Pageable inline keyboard for pyTelegramBotAPI.

A library for pyTelegramBotAPI that allows you to display data in the format of a pageable inline keyboard.
"""

from math import ceil
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

class Keyboard():
    """
    Keyboard:
        A class that handles InlineKeyboardMarkup (reply keyboard markup in pyTelegramBotAPI) buttons pagination.

    This is a documentation for the __init__ function of the class.
    Args:
        chat_id (int): The id of the chat that the message containing the inline keyboard was sent in.
        data (List[Tuple]): List of tuples containing ('button text', 'callback data') in this format.
        row_width (int): Number of buttons to show per row.
        rows_per_page (int): Number of rows to show per page.
        button_text_mode (int): The mode which the buttons texts will be displayed.
        text_index (int): The index of the button text in the tuples in the data list you provided.
        callback_index (int): The index of the callback data in the the tuples in the data list you provided.
        next_page (str): The content that will be shown in the next_page button.
        previous_page (str): The content that will be shown in the previous_page button.
    """

    def __init__(
        self, chat_id, data, row_width=1, rows_per_page=5, button_text_mode=0,
        text_index=0, callback_index=0, next_page='--->', previous_page='<---'
    ):
        self.chat_id = chat_id
        self.current_page = 0
        self.data = data
        self.count = len(self.data) / row_width
        self.pages = ceil(self.count/rows_per_page)
        self.rows_per_page = rows_per_page
        self.row_width = row_width
        self.button_text_mode = button_text_mode
        self.text_index = text_index
        self.callback_index = callback_index
        self.next_page = next_page
        self.previous_page = previous_page

    def text_callback(self):
        """
        text_callback: Generates the buttons for a single page. Determines content based on the self.current_page variable.

        Return:
            InlineKeyboardMarkup: object containing the button for the self.current_page.
        """
        keyboard = InlineKeyboardMarkup(row_width=self.row_width)
        buttons_per_page = self.rows_per_page * self.row_width
        page_data = self.data[
                self.current_page * buttons_per_page:
                self.current_page * buttons_per_page + buttons_per_page
            ]

        try:
            for i in range(0, len(page_data), self.row_width):
                button = []
                if self.button_text_mode == 1:
                    for j in range(0, self.row_width):
                        button.append(
                            InlineKeyboardButton(
                                text=page_data[i + j][self.text_index],
                                callback_data=page_data[i + j][self.callback_index]
                            )
                        )
                elif self.button_text_mode == 2:
                    for j in range(0, self.row_width):
                        button.append(
                            InlineKeyboardButton(
                                text=page_data[i + j][self.text_index] + ' (' + page_data[i + j][self.callback_index] + ')',
                                callback_data=page_data[i + j][self.callback_index]
                            )
                        )
                elif self.button_text_mode == 3:
                    for j in range(0, self.row_width):
                        button.append(
                            InlineKeyboardButton(
                                text=page_data[i + j][self.callback_index] + ' (' + page_data[i + j][self.text_index] + ')',
                                callback_data=page_data[i + j][self.callback_index]
                            )
                        )
                else:
                    for j in range(0, self.row_width):
                        button.append(
                            InlineKeyboardButton(
                                text=page_data[i + j][0],
                                callback_data=page_data[i + j][0]
                            )
                        )
                keyboard.row(*button)
        except IndexError as e:
            keyboard.row(*button)
            pass
        return keyboard

    def send_keyboard(self):
        """
        send_keyboard: Generates the first page of the keyboard.

        Return:
            InlineKeyboardMarkup: object containing the button for the self.current_page and navigation buttons if there are multiple pages.
        """
        keyboard = self.text_callback()

        if self.pages > 1:
            keyboard.row(
                    InlineKeyboardButton(text='-', callback_data='-'),
                    InlineKeyboardButton(
                        text=f'{1}/{self.pages}',
                        callback_data=f'{1}/{self.pages}'
                    ),
                    InlineKeyboardButton(
                        text=self.next_page,
                        callback_data='next_page'
                    )
                )
        return keyboard

    def edit_keyboard(self, call: CallbackQuery):
        """
        edit_keyboard: Edits keyboard pages when call from next_page and previous_page comes in.

        Args:
            call (CallbackQuery :obj:): The CallbackQuery object from the next_page or previous_page buttons.

        Return:
            InlineKeyboardMarkup: object containing the button for the self.current_page and navigation buttons.
        """
        if call.data == 'next_page' and self.current_page < self.pages:
            self.current_page = self.current_page + 1
        elif call.data == 'previous_page' and self.current_page > 0:
            self.current_page = self.current_page - 1

        keyboard = self.text_callback()

        if self.current_page == 0:
            keyboard.row(
                InlineKeyboardButton(text='-', callback_data='-'),
                InlineKeyboardButton(
                    text=f'{self.current_page+1}/{self.pages}',
                    callback_data=f'{self.current_page+1}/{self.pages}'
                ),
                InlineKeyboardButton(
                    text=self.next_page, callback_data='next_page'
                )
            )
        elif self.pages - self.current_page == 1:
            keyboard.row(
                InlineKeyboardButton(
                    text=self.previous_page, callback_data='previous_page'
                ),
                InlineKeyboardButton(
                    text=f'{self.current_page+1}/{self.pages}',
                    callback_data=f'{self.current_page+1}/{self.pages}'
                ),
                InlineKeyboardButton(text='-', callback_data='-')
            )
        else:
            keyboard.row(
                InlineKeyboardButton(
                    text=self.previous_page, callback_data='previous_page'
                ),
                InlineKeyboardButton(
                    text=f'{self.current_page+1}/{self.pages}',
                    callback_data=f'{self.current_page+1}/{self.pages}'
                ),
                InlineKeyboardButton(
                    text=self.next_page, callback_data='next_page'
                )
            )

        return keyboard