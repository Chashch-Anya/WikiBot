import types
import telebot
import wikipedia

# ссылка на бота t.me/wikis_new_bot

bot = telebot.TeleBot('')
global lang
lang = 'ru'

# ====================== comands ====================================
# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_full_name = message.from_user.full_name
    bot.send_message(message.chat.id, F"Привет, {user_full_name}! Я бот для поиска значения слов. С помощью команды /help вы можете узнать мои возможности\n Отправьте мне любое слово и я найду его значение в Wikipedia")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Я могу найти значение необходимого вам слова в Wikipedia. По умолчанию я ищу русские слова. Для смены языка введите /change_language")

@bot.message_handler(commands=['change_language'])
def help_message(message):
    markup = language_markup()
    bot.send_message(message.chat.id, text='Выберите язык для поиска слов', reply_markup=markup)
# ==================================================================

#===================== markup ======================================
# markup с валютами
def language_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    buttons_ru = telebot.types.InlineKeyboardButton(text='Русский', callback_data='ru')
    buttons_en = telebot.types.InlineKeyboardButton(text='Английский', callback_data='en')
    markup.add(buttons_ru,buttons_en)
    return markup

# def yes_or_no_markup():
#     markup = telebot.types.InlineKeyboardMarkup()
#     buttons_y = telebot.types.InlineKeyboardButton(text='Найти значение слова на просторах интернета', callback_data='Yes')
#     markup.add(buttons_y)
#     return markup 
# ==================================================================

# ===================== callbacks ======================================
@bot.callback_query_handler(func=lambda call: True)
def bot_query_handler(call):
    
    global lang
    if (call.data == "en"):
        lang = 'en'
        bot.answer_callback_query(callback_query_id=call.id, text="Смена языка.....")
        bot.send_message(call.message.chat.id, 'Язык поиска слов сменился на английский')
    elif (call.data == "ru") :
        lang = 'ru'
        bot.answer_callback_query(callback_query_id=call.id, text="Смена языка.....")
        bot.send_message(call.message.chat.id, 'Язык поиска слов сменился на русский')
    # elif (call.data == "Yes") :
        # bot.send_message(call.message.chat_id,f"""""")


# ==================================================================

# Поиск слова
@bot.message_handler(content_types=['text'])
def get_word_message(message):
    try:
        wikipedia.set_lang(lang)
        result = wikipedia.summary(str(message.text))
        web = wikipedia.page(str(message.text))
        
        bot.send_message(message.chat.id, text='Вот что я смог найти:')
        bot.send_message(message.chat.id, result)
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(
            text="Статья в википедии", url=str(web.url))
        markup.add(button1)
        bot.send_message(message.chat.id, "Ссылка на полную статью", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, text='К сожалению,  я не смог найти данное слово в базе Wikipedia')
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(
            text="Результаты поиска в Яндекс", url="""https://yandex.ru/search/?text="""
            + message.text.replace(' ', "+") +
            """&lr=50&search_source=yaru_desktop_common""")
        markup.add(button1)
        bot.send_message(
            message.chat.id, "Можете найти в интернете по ссылке:", reply_markup=markup)
bot.infinity_polling()


