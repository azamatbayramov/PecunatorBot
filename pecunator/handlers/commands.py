from bot.bot import bot
from utils import validators, utils
from database.models import Group, User, Operation
from database.database import Session
import datetime


@bot.message_handler(commands=["start"])
@validators.group_required
def start(message):
    telegram_id = message.chat.id

    if validators.is_registered_group(telegram_id):
        bot.reply_to(message, "This group has already been initialized.")
    else:
        session = Session()
        session.add(Group(telegram_id=telegram_id))
        session.commit()
        bot.reply_to(message, "This group has been initialized.")


@bot.message_handler(commands=["join"])
@validators.registered_group_required
def join_user(message):
    if validators.is_registered_user(message.chat.id, message.from_user.id):
        bot.reply_to(message, "You are already a member of this group")
    else:
        session = Session()
        session.add(User(telegram_id=message.from_user.id, group_id=message.chat.id, username=message.from_user.username, balance=0))
        session.commit()
        bot.reply_to(message, "You have been added to this group")


@bot.message_handler(commands=["buy"])
@validators.registered_group_required
@validators.registered_user_required
def buy(message):
    group_id = message.chat.id
    user_telegram_id = message.from_user.id

    command_lst = message.text.split()

    if len(command_lst) < 3:
        bot.reply_to(message, "Wrong format")
        return

    try:
        amount = int(command_lst[-1])
        label = ' '.join(command_lst[1:-2])
    except:
        bot.reply_to(message, "Wrong format")
        return

    if amount < 0:
        bot.reply_to(message, "Wrong amount")
        return

    session = Session()
    user = session.query(User).filter(User.telegram_id == user_telegram_id, User.group_id == group_id).first()
    user.balance += amount
    group = session.query(Group).filter(Group.telegram_id == group_id).first()
    group.total_balance += amount
    session.add(group)
    session.add(user)
    session.add(Operation(author_id=user.id, group_id=group_id, amount=amount, label=label, is_reset=False, datetime=datetime.datetime.now()))
    session.commit()

    bot.reply_to(message, f"New balances:\n{utils.get_balances_str(group_id)}")


@bot.message_handler(commands=["total"])
@validators.registered_group_required
def send_balances(message):
    group_id = message.chat.id

    balances_str = utils.get_balances_str(group_id)

    bot.reply_to(message, balances_str)


@bot.message_handler(commands=["reset"])
@validators.registered_group_required
@validators.registered_user_required
def reset(message):
    group_id = message.chat.id

    lst_command = message.text.split()

    if len(lst_command) != 2 or lst_command[1] != str(datetime.datetime.now().day):
        bot.reply_to(message, "Write please: /reset {today's day}")
        return

    bot.reply_to(message, f"Balances before reset:\n{utils.get_balances_str(group_id)}")

    session = Session()

    group = session.query(Group).filter(Group.telegram_id == group_id).first()

    for user in group.users:
        user.balance = 0
        session.add(user)

    group.total_balance = 0

    session.add(group)

    session.commit()
