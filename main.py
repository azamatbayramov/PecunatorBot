from dotenv import load_dotenv
load_dotenv()

import os
import telebot
import users

print(os.environ)

bot = telebot.TeleBot(os.environ["TELEGRAM_API_TOKEN"], parse_mode=None)


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


@bot.message_handler(commands=["join"])
def join_user(message):
    answer = users.edit_joined(message.from_user.id, message.from_user.username, 1)
    bot.reply_to(message, answer.format(message.from_user.username))


@bot.message_handler(commands=["leave"])
def leave_user(message):
    answer = users.edit_joined(message.from_user.id, message.from_user.username, 0)
    bot.reply_to(message, answer.format(message.from_user.username))


bot.infinity_polling()
