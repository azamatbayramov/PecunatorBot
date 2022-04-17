import telebot
import json

settings = json.load(open("settings.json", encoding="utf8"))

bot = telebot.TeleBot(settings["telegram_api_token"], parse_mode=None)


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


bot.infinity_polling()
