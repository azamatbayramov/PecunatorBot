from bot.bot import bot
from utils import validators
from database.models import Group
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



