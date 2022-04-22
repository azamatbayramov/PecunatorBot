from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import os
import telebot
import user
from utils import get_group_and_user

# This line should be placed before ANY logic
# Beware of imports that execute something immediately
load_dotenv()

firebase_cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "token_uri": "https://oauth2.googleapis.com/token",
})

firebase_admin.initialize_app(firebase_cred, {"databaseURL": os.environ["FIREBASE_DATABASE_URL"]})

bot = telebot.TeleBot(os.environ["TELEGRAM_API_TOKEN"], parse_mode=None)


def check_init(f):
    def rf(m):
        g, u = get_group_and_user(m)

        if not u.exists():
            u.init_user_in_db()

        if not g.exists():
            bot.reply_to(m, "This group is not initialized")
        else:
            f(m)
    return rf


@bot.message_handler(func=lambda message: message.chat.type != "group")
def send_welcome_in_not_group(message):
    bot.reply_to(message, "Hello. I work only in groups.\nAdd me to group and I'll work")


@bot.message_handler(commands=["start"])
def start(message):
    g, u = get_group_and_user(message)

    if not g.exists():
        g.init_in_db()
        bot.reply_to(message, "This group has been initialized. Welcome!")
    else:
        bot.reply_to(message, "This group has already been initialized.")


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(message, "Hey")


@bot.message_handler(commands=["join"])
@check_init
def join_user(message):
    g, u = get_group_and_user(message)

    if g.get_user(u):
        bot.reply_to(message, "You are already a member of this group")
    else:
        g.add_user(u)
        u.add_group(g)
        bot.reply_to(message, "You have been added to this group")


@bot.message_handler(commands=["leave"])
@check_init
def leave_user(message):
    g, u = get_group_and_user(message)

    if g.get_total_balance() == 0:
        if not g.get_user(u):
            bot.reply_to(message, "You are not in the group")
        else:
            g.delete_user(u)
            u.delete_group(g)

            bot.reply_to(message, "Goodbye! You have left the group")
    else:
        bot.reply_to(message, "You have to finish this period to leave the group")


@bot.message_handler(commands=["purchase"])
@check_init
def purchase(message):
    g, u = get_group_and_user(message)

    if not g.get_user(u):
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

    g.add_payment(u, amount, label)
    g.edit_user_balance(u, amount)
    total_balance = g.edit_total_balance(amount)
    u.edit_balance(g, amount)

    bot.reply_to(message, f"Purchase added. Total balance of group: {total_balance}")


@bot.message_handler(commands=["total"])
@check_init
def total(message):
    g, u = get_group_and_user(message)

    users = g.get_users()

    if users:
        lst = [f"Total balance: {g.get_total_balance()}", '']

        for user_id in users.keys():
            lst.append(f"@{users[user_id]['username']}: {users[user_id]['balance']}")

        bot.reply_to(message, '\n'.join(lst))
    else:
        bot.reply_to(message, "It's so deserted here")


@bot.message_handler(commands=["reset"])
@check_init
def reset(message):
    g, u = get_group_and_user(message)

    if not g.get_user(u):
        bot.reply_to(message, "User not added")
        return

    if g.get_total_balance() == 0:
        bot.reply_to(message, "Total balance is 0")
        return

    g.add_reset(u)

    for i in g.get_users():
        ui = user.User(i)
        g.reset_user_balance(ui)
        ui.reset_group_balance(g)

    g.reset_total_balance()

    bot.reply_to(message, "Reset completed")


print("Bot started!")
bot.infinity_polling()
