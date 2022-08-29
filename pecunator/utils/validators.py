from bot.bot import bot
from database.database import Session
from database.models import User, Group


def is_group(telegram_id: str):
    return int(telegram_id) < 0


def is_registered_group(telegram_id: str):
    return Session().query(Group).filter(Group.telegram_id == telegram_id).first()


def is_registered_user(group_id: str, user_id: str):
    return Session().query(User).filter(User.telegram_id == user_id, User.group_id == group_id).first()


def group_required(func):
    def wrapper(message):
        telegram_id = str(message.chat.id)
        if not is_group(telegram_id):
            bot.reply_to(message, "It's not a group")
            return
        func(message)

    return wrapper


def registered_group_required(func):
    def wrapper(message):
        telegram_id = str(message.chat.id)
        if not is_group(telegram_id):
            bot.reply_to(message, "It's not a group")
            return

        if not is_registered_group(telegram_id):
            bot.reply_to(message, "It's not a registered group")
            return

        func(message)

    return wrapper


def registered_user_required(func):
    def wrapper(message):
        group_id = str(message.chat.id)
        user_id = str(message.from_user.id)

        if not is_registered_user(group_id, user_id):
            bot.reply_to(message, "You're not joined")
            return

        func(message)

    return wrapper
