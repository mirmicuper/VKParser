from email import message
import telebot
import parser as pr
import datetime
bot = telebot.TeleBot("5584210992:AAEi9zE_tjkFQcTgJXfY9yNOUqgtgjQfyEo")
@bot.message_handler(commands=['start'])
def start_message(message):
    pr.clickStart()
    pr.razd()
    bot.send_message(message.chat.id,'Привет✌️\nЯ бот, который поможет определить город человека по ссылке на страницу в вк🌍\nВведи ссылку на страницу в вк в формате https://vk.com/')
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text[0:15] == 'https://vk.com/':
        pr.delInfoFromFile()
        pr.razd()
        user_id = pr.getID(message.text)
        waiting = bot.send_message(message.chat.id, 'Происходит анализ. ⏳Ждите...')
        pr.getInfo(user_id)
        top_city = pr.dataAnalisCityForBot()
        bot.edit_message_text(chat_id=message.chat.id, message_id=waiting.message_id, text="🏙Человек из города: " + str(top_city[0][0]))
    else:
        bot.reply_to(message, "❗️❗️❗️Введена неверная ссылка либо страница закрыта❗️❗️❗️")
bot.polling(none_stop=True, interval=0)