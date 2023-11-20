import telebot

from config import token


bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.infinity_polling()

