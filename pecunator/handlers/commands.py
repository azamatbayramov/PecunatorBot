import datetime

from bot.bot import bot
from utils import validators
from database.models import Group, User, Operation
from utils.validators import is_registered_user
from database.database import Session


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
    if is_registered_user(message.chat.id, message.from_user.id):
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
    bot.reply_to(message, str(command_lst))
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
    user = session.query(User).filter(User.telegram_id == user_telegram_id, Group.telegram_id == group_id).first()
    user.balance += amount
    session.add(user)
    session.add(Operation(author_id=user.id, group_id=group_id, amount=amount, label=label, is_reset=False, datetime=datetime.datetime.now()))
    session.commit()


@bot.message_handler(commands=["total"])
@validators.registered_group_required
def send_balances(message):
    group_id = message.chat.id

    session = Session()

    users = session.query(User).filter(User.group_id == group_id).all()

    answer = ''

    for user in users:
        answer += f'{user.username} - {user.balance}\n'

    bot.reply_to(message, answer)
