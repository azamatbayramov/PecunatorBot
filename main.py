import telebot
from all_json import SETTINGS
import users

bot = telebot.TeleBot(SETTINGS["telegram_api_token"], parse_mode=None)


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


@bot.message_handler(commands=["join"])
def join_user(message):
    users.join_user(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"User @{message.from_user.username} was joined")


@bot.message_handler(commands=["leave"])
def leave_user(message):
    users.leave_user(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"User @{message.from_user.username} was leaved")


bot.infinity_polling()
