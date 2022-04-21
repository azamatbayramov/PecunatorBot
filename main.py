from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials
import os
import telebot
import group
import user


firebase_cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "token_uri": "https://oauth2.googleapis.com/token",
})

firebase_admin.initialize_app(firebase_cred, {"databaseURL": os.environ["FIREBASE_DATABASE_URL"]})

bot = telebot.TeleBot(os.environ["TELEGRAM_API_TOKEN"], parse_mode=None)


def get_group_and_user(message):
    g = group.Group(
        message.chat.id,
        message.chat.title
    )

    u = user.User(
        message.from_user.id,
        message.from_user.username,
        f"{message.from_user.first_name}{' ' + message.from_user.last_name if message.from_user.last_name else ''})"
    )

    return g, u


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start"])
def init_group(message):
    response = group.Group(message.chat.id).init_group_in_db()
    bot.reply_to(message, response["message"])


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


@bot.message_handler(commands=["join"])
def join_user(message):
    g, u = get_group_and_user(message)

    if g.get_user(u.user_id):
        bot.reply_to(message, "User has already been added")
    else:
        g.add_user(u.user_id, u.username)
        u.add_group(g.group_id, g.group_name)

        bot.reply_to(message, "User added")


@bot.message_handler(commands=["leave"])
def leave_user(message):
    g, u = get_group_and_user(message)

    if g.get_total_balance() == 0:
        if not g.get_user(u.user_id):
            bot.reply_to(message, "User has already been deleted")
        else:
            g.delete_user(u.user_id)
            u.delete_group(g.group_id)

            bot.reply_to(message, "User deleted")
    else:
        bot.reply_to(message, "You have to finish this period to leave")


@bot.message_handler(commands=["purchase"])
def purchase(message):
    g, u = get_group_and_user(message)

    if not g.get_user(u.user_id):
        bot.reply_to(message, "User not added")
        return
    command_lst = message.text.split()

    if len(command_lst) < 3:
        bot.reply_to(message, "Wrong format")
        return

    try:
        amount = int(command_lst[1])
        label = ' '.join(command_lst[2:])
    except:
        bot.reply_to(message, "Wrong format")
        return

    g.add_payment(u.user_id, amount, label)
    g.edit_user_balance(u.user_id, amount)
    total_balance = g.edit_total_balance(amount)
    u.edit_balance(g.group_id, amount)

    bot.reply_to(message, f"Purchase added. Total balance of group: {total_balance}")


@bot.message_handler(commands=["total"])
def total(message):
    g, u = get_group_and_user(message)

    users = g.get_users()

    lst = []

    for user_id in users.keys():
        lst.append(f"@{users[user_id]['username']}: {users[user_id]['balance']}")

    bot.reply_to(message, '\n'.join(lst))


print("Bot started!")
bot.infinity_polling()
