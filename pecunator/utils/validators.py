from bot.bot import bot
from database.database import Session
from database.models import User, Group


def is_group(telegram_id: int):
    return telegram_id < 0


def is_registered_group(telegram_id: int):
    return Session().query(Group).filter(Group.telegram_id == telegram_id).first()


def is_registered_user(group_id, user_id):
    return Session().query(User).filter(User.telegram_id == user_id, Group.telegram_id == group_id).first()


def group_required(func):
    def wrapper(message):
        telegram_id = message.chat.id
        if not is_group(telegram_id):
            bot.reply_to(message, "It's not a group")
            return
        func(message)

    return wrapper
