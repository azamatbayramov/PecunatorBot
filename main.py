from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials
import os
import telebot
import group


firebase_cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "token_uri": "https://oauth2.googleapis.com/token",
})

firebase_admin.initialize_app(firebase_cred, {"databaseURL": os.environ["FIREBASE_DATABASE_URL"]})

bot = telebot.TeleBot(os.environ["TELEGRAM_API_TOKEN"], parse_mode=None)


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start"])
def init_group(message):
    response = group.Group(message.chat.id).init_group()
    bot.reply_to(message, response["message"])


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


@bot.message_handler(commands=["join"])
def join_user(message):
    answer = "TODO"#users.edit_joined(message.from_user.id, message.from_user.username, 1)
    bot.reply_to(message, answer.format(message.from_user.username))


@bot.message_handler(commands=["leave"])
def leave_user(message):
    answer = "TODO"#users.edit_joined(message.from_user.id, message.from_user.username, 0)
    bot.reply_to(message, answer.format(message.from_user.username))


print("Bot started!")
bot.infinity_polling()
