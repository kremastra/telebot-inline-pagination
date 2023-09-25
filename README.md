# Telegram Inline Paginator for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/) (telebot)

A library for pyTelegramBotAPI that allows you to easily do pagination for any Inline keyboards.

## Installation
You can use [pip](https://pip.pypa.io/en/stable/) to install this library.
```
pip install telebot-inline-pagination
```

## Steps
### Step 1. Import necessary libraries and connect Telegram token

```py
from api import bot # Telegram Token in the file api.py
from telebot.types import CallbackQuery
from telebot_inline_pagination import Keyboard
```

### Step 2. Define the parameters

### Required parameters

**data**: Dataset in "list of tuples" format, without headers.

**text_message**: Message displayed above the keyboard.

```py
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
```

### Optional parameters

**rows_per_page**: The number of rows of buttons on one page, excluding the navigation bar (by default - 5).

**text_index**: Column index - data source for button titles (by default - 0).

**callback_index**: Column index - data source for callback-function (by default - 0).

**button_text_mode**: The number of the mode responsible for the format of the displayed text on the buttons:
* 0 or None (by default) - The button displays data and has callback data from the column index 0
* 1 - The button displays only data from the **text_index** column
* 2 - The button displays data from the **text_index** column, and in brackets - data from the **callback_index** column
* 3 - The button displays data from the **callback_index** column, and in brackets - data from the **text_index** column

**next_page**: Content of the button to go to the next page (by default - '--->').

**previous_index**: Content of the button to go to the previous page (by default - '<---').

```py
text_index = 0 # in this example, full airport name
callback_index = 1 # in this example, IATA/ICAO airport code
button_text_mode = 2 # in this example, "full airport name (IATA/ICAO airport code)"
rows_per_page = 3
next_page = '--->'
previous_page = '<---'
```

### Step 3. Creating the pageable keyboard instance

The standard pageable keyboard instance looks like this:

```py
Keyboard(chat_id=message.chat.id, data=data, rows_per_page=rows_per_page, button_text_mode=button_text_mode, text_index=text_index, callback_index=callback_index, next_page='>', previous_page='<')
```

In this example, the instance is written to the variable **keyboards** to ensure multithreading:

```py
keyboards = []

...

    json = {"id": message.chat.id, "object": Keyboard(chat_id=message.chat.id, data=data, rows_per_page=rows_per_page, button_text_mode=button_text_mode, text_index=text_index, callback_index=callback_index)}
    keyboards.append(json)
```   

### Step 4. Creating the message handler for pageable keyboard

The standard message handler for pageable keyboard looks like this:

```py
bot.send_message(message.from_user.id, text_message, reply_markup=Keyboard.send_keyboard()
```

In this example, the keyboard calls using the **/start** command. Also, 
first, when using the **/start** command, all previously created instances are deleted. Second, a new instance is added to the message handler.

```py
@bot.message_handler(commands=['start'])
def demo_pagination(message):
    for i, j in enumerate(keyboards):
        if j["id"] == message.chat.id:
            del keyboards[i]    
    json = {"id": message.chat.id, "object": Keyboard(chat_id=message.chat.id, data=data, rows_per_page=rows_per_page, button_text_mode=2, text_index=0, callback_index=1)}
    keyboards.append(json)
    for i in keyboards:
        if i["id"] == message.chat.id:
            bot.send_message(message.from_user.id, text_message, reply_markup=i["object"].send_keyboard())
```

### Step 5. Creating the callback query handler for pageable keyboard

The standard callback query handler for pageable keyboard looks like this:

```py
bot.edit_message_text(text_message, reply_markup = Keyboard.edit_keyboard(call), chat_id = call.message.chat.id, message_id = call.message.message_id)
```

In this example, we use the current chat id to find the required instance in the **keyboards** list and launch the callback query handler. Also, we use the **send_message** command to receive a message with information when the result button is clicked.

```py
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
```

### Full example

In this example, the code implements multithreading: the bot can be used by several people at the same time without interfering with each other.

```py
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

text_index = 0
callback_index = 1
button_text_mode = 2
rows_per_page = 3
next_page = '--->'
previous_page = '<---'

keyboards = []

@bot.message_handler(commands=['start'])
def demo_pagination(message):
    for i, j in enumerate(keyboards):
        if j["id"] == message.chat.id:
            del keyboards[i]    
    json = {"id": message.chat.id, "object": Keyboard(chat_id=message.chat.id, data=data, rows_per_page=rows_per_page, button_text_mode=2, text_index=0, callback_index=1, next_page='>', previous_page='<')}
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
```

![button_text_mode.jpg](https://github.com/kremastra/telebot-inline-pagination/blob/main/img/button_text_mode.jpg?raw=true)

## License
[MIT](https://github.com/kremastra/telebot-inline-pagination/blob/main/LICENSE).