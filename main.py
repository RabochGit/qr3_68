import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6591236192:AAFM-cN-lgs1necK-7uKlfnAC3qzwdv9HmQ",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "опрос"  # Можно менять текст
text_button_1 = "Past Simple"  # Можно менять текст
text_button_2 = "Past Continuous"  # Можно менять текст
text_button_3 = "Past Perfect"  # Можно менять текст
text_button_4 = "Past Perfect Continuous"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        '_Привет! Как давно ты учишь английский язык?_',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id,
                     '_Супер! Ты хочешь узнать больше про Past tenses в английском языке?_ ')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,
                     '_Надеюсь, что да. Тогда нажимай на кнопки и получай ссылки на крутые видео на тему past tenses_')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'УЧИ АНГЛИЙСКИЙ!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Видео про Past Simple](https://youtu.be/efgHWkcDfIs?feature=shared)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Видео про Past Continuous] (https://youtu.be/5X4RyylTILI?feature=shared)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Видео пpо Past Rerfect](https://youtu.be/WGQcstYOhfs?feature=shared)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_4 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Видео про Past Perfect Continuous](https://youtu.be/TU78I3CRVlY?feature=shared)",
                     reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

